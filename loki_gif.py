"""
Loki 桌宠 - 配置驱动版本
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

from core.registry import ActionRegistry
from core.scheduler import ActionScheduler
from core.window import PetWindow


def get_base_path():
    """获取资源基础路径（支持 PyInstaller 打包）"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def main():
    app = QApplication(sys.argv)

    # 创建组件
    base_path = get_base_path()
    config_path = os.path.join(base_path, "actions.json")
    registry = ActionRegistry(config_path)
    scheduler = ActionScheduler(registry)
    window = PetWindow(registry, scheduler)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()