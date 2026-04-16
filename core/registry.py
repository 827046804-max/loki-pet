"""
动作注册表：加载配置 + 预加载资源
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from PyQt5.QtGui import QMovie

from .action import ActionConfig, ActionResource


# 默认配置（配置文件损坏时的 fallback）
DEFAULT_CONFIG = {
    "default": "stay",
    "idle_interval": 3.0,
    "actions": {
        "stay": {
            "path": "images/loki_stay.gif",
            "label": "静止",
            "kind": "loop",
            "triggers": ["menu"],
            "menu_order": 1,
            "interruptible": True,
            "cooldown": 0
        },
        "play": {
            "path": "images/loki_play.gif",
            "label": "玩耍",
            "kind": "oneshot",
            "next": "stay",
            "max_loops": 3,
            "triggers": ["menu", "idle"],
            "menu_order": 2,
            "weight": 30,
            "cooldown": 5,
            "interruptible": True
        },
        "walk": {
            "path": "images/loki_walk.gif",
            "label": "走路",
            "kind": "loop",
            "triggers": ["menu", "idle"],
            "menu_order": 3,
            "weight": 40,
            "cooldown": 3,
            "interruptible": True,
            "duration": 8,
            "move_speed": 2
        },
        "jump": {
            "path": "images/loki_jump.gif",
            "label": "跳跃",
            "kind": "oneshot",
            "next": "stay",
            "max_loops": 1,
            "triggers": ["menu"],
            "menu_order": 4,
            "interruptible": False,
            "cooldown": 2
        }
    }
}


class ActionRegistry:
    """动作注册表：配置 + 资源"""

    def __init__(self, config_path: str = "actions.json"):
        self.config_path = Path(config_path)
        # 基于配置文件所在目录解析相对路径
        self.base_dir = self.config_path.parent.resolve()
        self.configs: Dict[str, ActionConfig] = {}
        self.resources: Dict[str, ActionResource] = {}
        self.default: str = "stay"
        self.idle_interval: float = 3.0

        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = DEFAULT_CONFIG
        except (json.JSONDecodeError, FileNotFoundError):
            data = DEFAULT_CONFIG

        self.default = data.get("default", "stay")
        self.idle_interval = data.get("idle_interval", 3.0)

        actions_data = data.get("actions", {})
        for name, cfg in actions_data.items():
            self.configs[name] = ActionConfig(
                name=name,
                path=cfg.get("path", ""),
                label=cfg.get("label", name),
                kind=cfg.get("kind", "loop"),
                triggers=cfg.get("triggers", []),
                menu_order=cfg.get("menu_order", 0),
                next=cfg.get("next"),
                max_loops=cfg.get("max_loops", 0),
                cooldown=cfg.get("cooldown", 0.0),
                interruptible=cfg.get("interruptible", True),
                weight=cfg.get("weight", 0),
                anchor=cfg.get("anchor", "bottom_center"),
                duration=cfg.get("duration", 0.0),
                move_speed=cfg.get("move_speed", 0)
            )

    def load_movies(self):
        """预加载所有 QMovie"""
        for name, cfg in self.configs.items():
            # 相对路径基于配置文件所在目录解析
            path = self.base_dir / cfg.path
            if path.exists():
                movie = QMovie(str(path))
                movie.setCacheMode(QMovie.CacheAll)
                self.resources[name] = ActionResource(movie=movie)
            else:
                print(f"[Warning] 动作 '{name}' 资源不存在: {path}")

    def get(self, name: str) -> Optional[ActionConfig]:
        """获取动作配置"""
        return self.configs.get(name)

    def get_resource(self, name: str) -> Optional[ActionResource]:
        """获取动作资源"""
        return self.resources.get(name)

    def get_movie(self, name: str) -> Optional[QMovie]:
        """获取 QMovie 实例"""
        res = self.resources.get(name)
        return res.movie if res else None

    def get_menu_actions(self) -> List[ActionConfig]:
        """获取菜单显示的动作（按 menu_order 排序）"""
        menu_actions = [
            cfg for cfg in self.configs.values()
            if "menu" in cfg.triggers
        ]
        return sorted(menu_actions, key=lambda a: a.menu_order)

    def get_idle_actions(self) -> List[ActionConfig]:
        """获取空闲触发的动作（过滤掉资源不存在的）"""
        return [
            cfg for cfg in self.configs.values()
            if "idle" in cfg.triggers and cfg.weight > 0 and cfg.name in self.resources
        ]

    def get_default(self) -> str:
        """获取默认动作名"""
        return self.default
