"""
动作调度器：选择动作 + 管理运行时状态
"""

import time
import random
from typing import Dict, List, Optional

from .action import ActionConfig
from .registry import ActionRegistry


class ActionScheduler:
    """动作调度器：选择 + 状态"""

    def __init__(self, registry: ActionRegistry):
        self.registry = registry
        self.current: str = registry.get_default()
        self.last_triggered: Dict[str, float] = {}

    def select(self, trigger: str, name: Optional[str] = None) -> Optional[str]:
        """
        选择动作

        Args:
            trigger: 触发方式 ("menu", "idle", "fallback")
            name: 指定动作名（menu 触发时使用）

        Returns:
            动作名，如果无法触发则返回 None
        """
        if trigger == "menu" and name:
            cfg = self.registry.get(name)
            if cfg and self.can_trigger(cfg):
                return name

        elif trigger == "idle":
            return self._select_idle()

        elif trigger == "fallback":
            return self._select_fallback()

        return None

    def can_trigger(self, cfg: ActionConfig) -> bool:
        """检查动作是否可以触发（冷却 + 可打断性）"""
        current_cfg = self.registry.get(self.current)

        # 检查当前动作是否可打断
        if current_cfg and not current_cfg.interruptible:
            if self.current != cfg.name:
                return False

        # 检查冷却
        now = time.time()
        last = self.last_triggered.get(cfg.name, 0.0)
        if now - last < cfg.cooldown:
            return False

        return True

    def mark_triggered(self, name: str):
        """标记动作已触发（更新冷却时间）"""
        self.last_triggered[name] = time.time()
        self.current = name

    def _select_idle(self) -> Optional[str]:
        """按权重随机选择空闲动作"""
        idle_actions = self.registry.get_idle_actions()
        if not idle_actions:
            return None

        # 过滤掉冷却中的动作
        available = [a for a in idle_actions if self.can_trigger(a)]
        if not available:
            return None

        # 按权重随机选择
        total_weight = sum(a.weight for a in available)
        if total_weight <= 0:
            return None

        r = random.randint(1, total_weight)
        accumulated = 0
        for cfg in available:
            accumulated += cfg.weight
            if r <= accumulated:
                return cfg.name

        return available[0].name

    def _select_fallback(self) -> str:
        """获取 oneshot 的回退动作"""
        current_cfg = self.registry.get(self.current)
        if current_cfg and current_cfg.next:
            return current_cfg.next
        return self.registry.get_default()
