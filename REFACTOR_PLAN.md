# Loki 桌宠动作系统重构方案

## 一、设计目标

| 目标 | 说明 |
|------|------|
| **配置驱动** | 动作定义与代码分离，加动作只需改配置 |
| **可扩展** | 轻松添加新动作、新触发方式 |
| **行为自然** | 待机随机、动作回退、冷却机制 |
| **易于维护** | 模块化，职责清晰 |
| **职责分离** | 选动作 vs 播放动作 vs 渲染窗口，互不干扰 |

---

## 二、新文件结构

```
loki-pet/
├── loki_gif.py              # 主入口（精简后）
├── actions.json             # 动作配置文件（核心）
├── core/
│   ├── __init__.py
│   ├── action_registry.py   # 读配置、校验、加载资源
│   ├── action_scheduler.py  # 选动作（权重/冷却/类别）
│   ├── action_player.py     # 切换 QMovie、监听结束、处理 next
│   └── pet_window.py        # 窗口、菜单、拖拽、渲染
├── images/
│   ├── loki_stay.gif
│   ├── loki_play.gif
│   ├── loki_jump.gif
│   └── ... (更多动作资源)
└── sounds/                  # 音效资源（可选）
    └── ...
```

---

## 三、动作配置结构 (actions.json)

```json
{
  "meta": {
    "default_action": "stay",
    "idle_check_interval": 3.0,
    "idle_trigger_chance": 0.3
  },

  "actions": {
    "stay": {
      "path": "images/loki_stay.gif",
      "label": "静止",
      "kind": "loop",
      "visible_in_menu": true,
      "idle_enabled": false,
      "interruptible": true,
      "anchor": "bottom_center",
      "sound": null
    },

    "play": {
      "path": "images/loki_play.gif",
      "label": "玩耍",
      "kind": "loop",
      "visible_in_menu": true,
      "idle_enabled": true,
      "weight": 40,
      "cooldown": 5,
      "interruptible": true,
      "anchor": "bottom_center",
      "sound": null
    },

    "jump": {
      "path": "images/loki_jump.gif",
      "label": "跳跃",
      "kind": "oneshot",
      "visible_in_menu": true,
      "idle_enabled": false,
      "interruptible": false,
      "next": "stay",
      "anchor": "bottom_center",
      "sound": "sounds/jump.wav"
    },

    "blink": {
      "path": "images/loki_blink.gif",
      "label": "眨眼",
      "kind": "oneshot",
      "visible_in_menu": false,
      "idle_enabled": true,
      "weight": 30,
      "cooldown": 3,
      "interruptible": true,
      "next": "stay",
      "anchor": "bottom_center",
      "sound": null
    },

    "stretch": {
      "path": "images/loki_stretch.gif",
      "label": "伸懒腰",
      "kind": "oneshot",
      "visible_in_menu": false,
      "idle_enabled": true,
      "weight": 15,
      "cooldown": 10,
      "interruptible": true,
      "next": "stay",
      "anchor": "bottom_center",
      "sound": null
    }
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `path` | string | ✅ | GIF 资源路径 |
| `label` | string | ✅ | 菜单显示名称 |
| `kind` | string | ✅ | `loop` 循环 / `oneshot` 一次性 |
| `visible_in_menu` | bool | ✅ | 是否在右键菜单显示 |
| `idle_enabled` | bool | ✅ | 是否可被空闲自动触发 |
| `interruptible` | bool | ✅ | 是否可被其他动作打断 |
| `weight` | int |  | 空闲触发权重（仅 idle_enabled=true 时有效） |
| `cooldown` | float |  | 冷却时间（秒） |
| `next` | string |  | oneshot 播完后回退的动作名 |
| `anchor` | string |  | 锚点位置：`bottom_center` / `center` / 自定义 |
| `sound` | string |  | 可选，音效路径 |

### 关键设计点

1. **`visible_in_menu` 和 `idle_enabled` 分离**
   - `blink` 不在菜单显示，但空闲时自动触发
   - `jump` 在菜单显示，但不自动触发
   - `stay` 在菜单显示，但不自动触发

2. **`anchor` 锚点机制**
   - 不同尺寸 GIF 切换时，用锚点对齐防止"跳动"
   - 默认 `bottom_center`，脚底居中对齐

---

## 四、核心类设计（四层分离）

### 职责边界表

| 类 | 职责 | 不负责 |
|----|------|--------|
| **ActionRegistry** | 加载配置、校验 schema、预加载 QMovie | 状态判断、动作选择、播放 |
| **ActionScheduler** | 选动作（权重随机、冷却检查、类别过滤） | 播放、窗口、资源管理 |
| **ActionPlayer** | 切换 QMovie、监听结束、处理 next | 选择逻辑、窗口 |
| **PetWindow** | 渲染、菜单、拖拽、接收用户输入 | 动作逻辑、播放控制 |

### 4.1 Action（动作数据类）

```python
@dataclass
class Action:
    # 配置字段
    name: str
    path: str
    label: str
    kind: str               # "loop" | "oneshot"
    visible_in_menu: bool
    idle_enabled: bool
    interruptible: bool
    weight: int
    cooldown: float
    next_action: Optional[str]
    anchor: str
    sound: Optional[str]

    # 运行时状态（不在配置中）
    last_triggered: float = 0.0
    movie: Optional[QMovie] = None
```

### 4.2 ActionRegistry（动作注册表）

```python
class ActionRegistry:
    """管理所有已注册的动作，只负责加载和查询"""

    def __init__(self, config_path: str):
        self.actions: Dict[str, Action] = {}
        self.meta: Dict = {}
        self._load_config(config_path)

    def _load_config(self, path: str):
        """从 JSON 加载动作配置，校验 schema"""

    def _validate_action(self, name: str, data: dict) -> bool:
        """校验单个动作配置是否合法"""

    def get(self, name: str) -> Optional[Action]:
        """获取动作"""

    def get_all(self) -> Dict[str, Action]:
        """获取所有动作"""

    def get_menu_actions(self) -> List[Action]:
        """获取 visible_in_menu=true 的动作"""

    def get_idle_actions(self) -> List[Action]:
        """获取 idle_enabled=true 的动作"""

    def load_movies(self):
        """预加载所有 QMovie 资源"""
```

### 4.3 ActionScheduler（动作调度器）

```python
class ActionScheduler:
    """只负责"选哪个动作"，不管播放"""

    def __init__(self, registry: ActionRegistry):
        self.registry = registry

    def select_by_name(self, name: str) -> Optional[str]:
        """按名称选择动作（用户点击菜单时用）"""

    def select_random_idle(self) -> Optional[str]:
        """空闲时按权重随机选择动作"""

    def can_trigger(self, action: Action, current: Optional[Action]) -> bool:
        """检查动作是否可触发：冷却 + 可打断性"""

    def get_fallback_action(self, from_action: Action) -> str:
        """获取 oneshot 动作的回退动作"""
```

### 4.4 ActionPlayer（动作播放器）

```python
class ActionPlayer(QObject):
    """只负责播放动作，管 QMovie 生命周期"""

    action_changed = pyqtSignal(str)  # 动作切换信号
    action_finished = pyqtSignal(str) # oneshot 播完信号

    def __init__(self, registry: ActionRegistry):
        self.registry = registry
        self.current_action: Optional[Action] = None

    def play(self, action_name: str) -> bool:
        """播放指定动作，返回是否成功"""

    def stop(self):
        """停止当前动作"""

    def get_current_movie(self) -> Optional[QMovie]:
        """获取当前 QMovie"""

    def get_current_pixmap(self) -> QPixmap:
        """获取当前帧"""

    def _on_movie_finished(self):
        """QMovie 播放完成回调"""
```

### 4.5 PetWindow（窗口类）

```python
class PetWindow(QWidget):
    """桌宠窗口，处理渲染和用户交互"""

    def __init__(self, registry: ActionRegistry, scheduler: ActionScheduler, player: ActionPlayer):
        self.registry = registry
        self.scheduler = scheduler
        self.player = player

        # 连接信号
        self.player.action_changed.connect(self._on_action_changed)
        self.player.action_finished.connect(self._on_action_finished)

    def paintEvent(self, event):
        """绘制当前帧"""

    def mousePressEvent(self, event):
        """点击交互：左键拖拽，右键菜单"""

    def show_menu(self, pos):
        """显示右键菜单（从 registry.get_menu_actions() 动态生成）"""

    def _on_action_finished(self, action_name: str):
        """oneshot 动作播完，请求调度器选择回退动作"""

    def _on_idle_timer(self):
        """空闲定时器触发，请求调度器选择随机动作"""
```

---

## 五、数据流

### 5.1 启动流程

```
main()
  ↓
ActionRegistry(config_path)  →  加载 actions.json，校验 schema
  ↓
registry.load_movies()       →  预加载所有 QMovie
  ↓
ActionScheduler(registry)    →  调度器初始化
  ↓
ActionPlayer(registry)       →  播放器初始化
  ↓
PetWindow(registry, scheduler, player)
  ↓
player.play("stay")          →  播放默认动作
  ↓
启动 idle 定时器
```

### 5.2 空闲触发流程

```
idle 定时器触发
  ↓
PetWindow._on_idle_timer()
  ↓
action_name = scheduler.select_random_idle()
  ↓
if action_name:
    player.play(action_name)
  ↓
oneshot 播完 → player.action_finished.emit()
  ↓
PetWindow._on_action_finished()
  ↓
fallback = scheduler.get_fallback_action(action)
  ↓
player.play(fallback)
```

### 5.3 菜单触发流程

```
右键点击
  ↓
PetWindow.show_menu()
  ↓
menu_actions = registry.get_menu_actions()
  ↓
动态生成菜单项
  ↓
用户选择 → scheduler.select_by_name(name)
  ↓
检查 can_trigger(action, current)
  ↓
player.play(action_name)
```

### 5.4 关键：职责分离

```
┌─────────────────────────────────────────────────────────────┐
│                      PetWindow                               │
│  (渲染、菜单、拖拽、定时器)                                    │
│                                                              │
│   idle_timer ──→ scheduler.select_random_idle() ──→ player  │
│   menu_click ──→ scheduler.select_by_name() ──────→ player  │
│   player.action_finished ──→ scheduler.get_fallback()       │
│                           ──→ player.play()                  │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │ Registry │    │Scheduler │    │  Player  │
       │ 资源管理  │    │ 选择动作  │    │ 播放动作  │
       └──────────┘    └──────────┘    └──────────┘
```

---

## 六、开发计划

### Phase 1：结构重构（优先级最高）

**硬要求：现有 stay / play / jump 行为完全不变**

| 步骤 | 任务 | 预计代码量 |
|------|------|------------|
| 1.1 | 创建 `actions.json` 配置文件 | ~50 行 |
| 1.2 | 创建 `core/` 目录和 `Action` 数据类 | ~40 行 |
| 1.3 | 实现 `ActionRegistry` 类（加载 + 校验 + 查询） | ~100 行 |
| 1.4 | 实现 `ActionPlayer` 类（QMovie 播放） | ~60 行 |
| 1.5 | 实现 `ActionScheduler` 类（select_by_name） | ~30 行 |
| 1.6 | 重构 `loki_gif.py` 主入口 | ~80 行 |
| 1.7 | 创建 `PetWindow` 类（从 loki_gif.py 抽离） | ~60 行 |

**完成标志**：
- 现有功能（stay/play/jump 菜单切换）完全不变
- 右键菜单从配置动态生成
- 代码量不变，但结构清晰

### Phase 2：轻量调度系统

| 步骤 | 任务 | 预计代码量 |
|------|------|------------|
| 2.1 | 实现 `select_random_idle()`（权重随机） | ~40 行 |
| 2.2 | 实现 `can_trigger()`（冷却 + 可打断检查） | ~30 行 |
| 2.3 | 实现 `get_fallback_action()`（oneshot 回退） | ~15 行 |
| 2.4 | PetWindow 增加 idle 定时器 | ~20 行 |
| 2.5 | Player 增加 `action_finished` 信号 | ~15 行 |
| 2.6 | 补充 blink / stretch 动作配置 | ~20 行 |

**完成标志**：
- 空闲时自动触发 blink/stretch 等小动作
- oneshot 动作播完自动回退到 stay
- 冷却时间生效

### Phase 3：交互增强

| 步骤 | 任务 |
|------|------|
| 3.1 | 左键点击触发随机反应动作 |
| 3.2 | 双击触发特殊动作 |
| 3.3 | 拖拽时播放"被抓住"动作（可选） |
| 3.4 | 增加 `anchor` 锚点机制，防止尺寸切换跳动 |

### Phase 4：动作资源扩充

| 类型 | 动作 | 优先级 | 帧数建议 |
|------|------|--------|----------|
| 小动作 | blink, stretch, yawn, look_around | 高 | 2-6 帧 |
| 情绪动作 | happy, sad, angry | 中 | 8-12 帧 |
| 互动动作 | pet, feed, play_dead | 中 | 8-16 帧 |
| 特殊动作 | sleep, wake_up | 低 | 16+ 帧 |

---

## 七、API 速览

```python
# === ActionRegistry ===
registry = ActionRegistry("actions.json")
registry.load_movies()
action = registry.get("blink")
menu_actions = registry.get_menu_actions()
idle_actions = registry.get_idle_actions()

# === ActionScheduler ===
action_name = scheduler.select_by_name("jump")
action_name = scheduler.select_random_idle()
can = scheduler.can_trigger(action, current_action)
fallback = scheduler.get_fallback_action(action)

# === ActionPlayer ===
player.play("blink")
player.stop()
movie = player.get_current_movie()
pixmap = player.get_current_pixmap()

# 信号
player.action_changed.connect(...)   # 动作切换
player.action_finished.connect(...)  # oneshot 播完
```

---

## 八、风险与应对

| 风险 | 应对 |
|------|------|
| GIF 资源不足 | 先用占位图或现有 GIF，逻辑先跑通 |
| QMovie 帧数检测不准 | 加 frameCount 校验，oneshot 用 finished 信号 |
| 动作切换闪烁 | 直接切换，后续可加淡入淡出 |
| 配置文件损坏 | 加默认配置回退，或硬编码最小配置 |
| 不同尺寸 GIF 跳动 | anchor 锚点机制，底部对齐 |

---

## 九、后续扩展方向

1. **状态机**：hungry → 索食动作，sleepy → 打哈欠
2. **行为树**：更复杂的决策逻辑
3. **日程系统**：不同时间段不同行为
4. **互动扩展**：跟随鼠标、躲避点击
5. **多角色**：支持多个桌宠同时运行
6. **音效系统**：动作配对音效

---

**预计总代码量**：~400 行核心代码（不含资源）

**开发顺序建议**：Phase 1 → Phase 2 → 补动作资源 → Phase 3 → Phase 4

**最小可用版本**：Phase 1 完成后，现有功能不变，但可扩展性具备
