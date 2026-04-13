# Loki 桌宠项目日志

## 2026-04-13 工作记录

### 项目背景
- 项目来自另一台电脑（Windows），需要继续在 macOS 上开发
- 原始仓库：https://github.com/827046804-max/loki-pet

### 完成的工作

#### 1. 项目克隆与分析
- 克隆项目到本地 `/Users/xair/loki-pet`
- 分析项目结构：
  - `loki_pet.py` - Python/tkinter Windows 版桌宠
  - `parts_data.py` - 像素部件数据
  - `index.html` + `js/` - Web 版预览

#### 2. 跨平台兼容问题解决
- **问题**：Windows tkinter 使用 `-transparentcolor` 实现透明窗口，macOS 不支持
- **解决方案**：使用 PyQt5 替代 tkinter
- **结果**：成功实现 macOS 透明窗口

#### 3. GIF 状态切换功能
- 用户提供了多张 GIF 动画图片
- 实现了状态切换系统：静止 → 玩耍 → 跳跃
- 创建了 `test_loki.py` 测试版本

#### 4. 当前文件结构
```
loki-pet/
├── images/
│   ├── loki_stay.gif    # 静止状态
│   ├── loki_play.gif    # 玩耍状态
│   └── loki_jump.gif    # 跳跃状态
├── loki_pet.py          # 原始 Windows 版（未修改）
├── parts_data.py        # 原始像素数据（未修改）
├── test_loki.py         # macOS 测试版（PyQt5）
└── loki_cross_platform.py  # 跨平台框架
```

---

## 沟通问题分析与改进

### 遇到的问题

| 问题 | 原因 | 改进建议 |
|------|------|----------|
| 像素数据不准确 | 我凭估算创建数据，没有精确提取 | 应先用代码分析图片像素，再生成数据 |
| 没有备份原版本 | 直接修改原文件 | 修改前先 `git status`，保持原版不动 |
| 误解用户需求 | 把"猫动"理解成"窗口移动" | 先确认理解：复述需求，问清楚再动手 |
| 进程管理混乱 | 多次启动导致窗口不显示 | 用户看不到效果时，先问是否看到，再调整 |

### 改进后的沟通流程

```
用户提出需求
    ↓
1. 复述确认理解（"你的意思是...对吗？"）
    ↓
2. 提供方案选项（如果有多种实现方式）
    ↓
3. 用户确认后再动手
    ↓
4. 完成后询问效果（"你能看到吗？有什么问题？"）
    ↓
5. 根据反馈调整
```

### 关于跨平台桌宠开发

**Windows vs macOS 关键差异：**
- 透明窗口：Windows 用 `-transparentcolor`，macOS 用 `-transparent` 或 PyQt 的 `WA_TranslucentBackground`
- 系统托盘：实现方式不同
- 推荐方案：使用 PyQt5/PySide 实现跨平台兼容

### 下一步计划

- [ ] 添加更多状态 GIF（睡觉、走路等）
- [ ] 完善状态切换逻辑（自动切换、随机切换）
- [ ] 添加互动功能（点击反应、音效）
- [ ] 打包发布版本

---

## 技术笔记

### PyQt5 加载 GIF 动画
```python
movie = QMovie('path/to.gif')
movie.setCacheMode(QMovie.CacheAll)
movie.start()
# 通过 frameChanged 信号更新显示
movie.frameChanged.connect(self.update)
```

### PyQt5 透明窗口设置
```python
self.setWindowFlags(
    Qt.FramelessWindowHint |
    Qt.WindowStaysOnTopHint |
    Qt.Tool
)
self.setAttribute(Qt.WA_TranslucentBackground)
```

---

## 如何更好地提问 - 用户指南

### 描述问题时可以包含的信息

1. **目标** - "我想实现什么效果"
   - 例：我想让猫在屏幕上到处走动

2. **现状** - "现在是什么情况"
   - 例：现在猫只会静止不动

3. **具体行为** - "具体应该怎样"
   - 例：猫应该每3秒随机改变方向，碰到屏幕边缘就转向

### 提问模板

```
【目标】我想让 Loki 有 XXX 功能
【现状】目前只能做到 XXX
【期望】具体效果是 XXX
【疑问】这个能实现吗？有什么条件？
```

### 常见场景的提问示例

**场景1：想添加新动作**
- ❌ "能不能让它动起来？"（太模糊）
- ✅ "我想添加一个'跳跃'动作，用户点击后猫会跳一下，跳完回到静止状态。需要准备什么素材？"

**场景2：想改变行为**
- ❌ "猫不动啊"（我可能理解成窗口不动或GIF不动）
- ✅ "我想让猫在屏幕上随机移动位置（窗口移动），而不是原地做动作"

**场景3：跨平台问题**
- ❌ "为什么跑不起来"
- ✅ "我在 Mac 上运行，报错 XXX，这个项目是在 Windows 上开发的，有兼容问题吗？"

### 我会主动做的事

1. **确认理解** - 用自己的话复述你的需求
2. **提供选项** - 有多种方案时，列出优缺点让你选
3. **说明条件** - 告诉你需要准备什么（素材、环境等）
4. **分步执行** - 大任务拆成小步骤，每步确认后再继续

---

## 下次启动命令

```bash
cd /Users/xair/loki-pet
/usr/bin/python3 test_loki.py
```
