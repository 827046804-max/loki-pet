"""
动作数据结构定义
"""

from dataclasses import dataclass, field
from typing import List, Optional
from PyQt5.QtGui import QMovie


@dataclass
class ActionConfig:
    """动作静态配置（从 JSON 加载）"""
    name: str
    path: str
    label: str
    kind: str  # "loop" | "oneshot"
    triggers: List[str]
    menu_order: int = 0
    next: Optional[str] = None
    max_loops: int = 0  # 0 = 无限循环
    cooldown: float = 0.0
    interruptible: bool = True
    weight: int = 0
    anchor: str = "bottom_center"
    duration: float = 0.0  # loop 类型动作的超时时长（秒），0 表示不超时
    move_speed: int = 0  # 走路速度（像素/帧），0 表示不移动


@dataclass
class ActionResource:
    """动作资源（QMovie 实例）"""
    movie: QMovie
