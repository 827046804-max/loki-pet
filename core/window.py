"""
桌宠窗口：播放 + 渲染 + 交互
"""

from PyQt5.QtWidgets import QWidget, QMenu, QApplication
from PyQt5.QtGui import QPainter, QCursor, QColor, QTransform
from PyQt5.QtCore import Qt, QTimer

from .registry import ActionRegistry
from .scheduler import ActionScheduler


class PetWindow(QWidget):
    """桌宠窗口"""

    def __init__(self, registry: ActionRegistry, scheduler: ActionScheduler):
        super().__init__()

        self.registry = registry
        self.scheduler = scheduler

        # 窗口属性 - 完全无边框透明 + 置顶
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("background: transparent;")

        # 当前 QMovie
        self._current_movie = None

        # 定时器（必须在 _play 之前初始化）
        self._loop_timeout_timer = QTimer(self)
        self._loop_timeout_timer.setSingleShot(True)
        self._loop_timeout_timer.timeout.connect(self._on_loop_timeout)

        self._idle_timer = QTimer(self)
        self._idle_timer.timeout.connect(self._on_idle)

        # 拖拽状态
        self._drag_pos = None

        # oneshot 循环检测
        self._loop_count = 0
        self._last_frame_num = -1

        # 走路移动
        self._move_direction = 1  # 1=右, -1=左

        # 加载资源并播放默认动作
        self.registry.load_movies()
        default_name = self.scheduler.current
        self._play(default_name)

        # 定位到屏幕右下角
        self._position_window()

        # 启动空闲定时器
        self._idle_timer.start(int(self.registry.idle_interval * 1000))

        # 显示窗口
        self.show()

    def _position_window(self):
        """定位窗口到屏幕右下角"""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 50
        y = screen.height() - self.height() - 100
        self.move(x, y)

    def _play(self, name: str):
        """播放动作"""
        movie = self.registry.get_movie(name)
        cfg = self.registry.get(name)
        if not movie:
            print(f"[Warning] 动作 '{name}' 资源不存在")
            return

        # 停止当前动画
        if self._current_movie:
            self._current_movie.stop()
            try:
                self._current_movie.frameChanged.disconnect(self._on_frame_changed)
                self._current_movie.finished.disconnect(self._on_movie_finished)
            except (TypeError, RuntimeError):
                pass

        self._current_movie = movie
        self.scheduler.mark_triggered(name)

        # 停止超时定时器
        self._loop_timeout_timer.stop()

        # 重置循环计数
        self._loop_count = 0
        self._last_frame_num = -1

        # 连接信号
        self._current_movie.frameChanged.connect(self._on_frame_changed)
        self._current_movie.finished.connect(self._on_movie_finished)

        self._current_movie.start()

        # 等待第一帧加载（最多尝试 100 次）
        attempts = 0
        while self._current_movie.currentPixmap().isNull() and attempts < 100:
            self._current_movie.jumpToNextFrame()
            attempts += 1

        if self._current_movie.currentPixmap().isNull():
            print(f"[Error] 动作 '{name}' 加载失败")
            return

        size = self._current_movie.currentPixmap().size()
        self.setFixedSize(size)

        # 对于 loop 类型动作，启动超时定时器
        if cfg and cfg.kind == "loop" and cfg.duration > 0:
            self._loop_timeout_timer.start(int(cfg.duration * 1000))

        self.update()

    def _on_frame_changed(self):
        """帧更新回调"""
        self.update()

        cfg = self.registry.get(self.scheduler.current)
        if not cfg:
            return

        # 走路时移动窗口
        if cfg.move_speed > 0:
            self._move_window(cfg.move_speed)

        # 检测 oneshot 循环完成（GIF 自带循环，finished 信号不触发）
        if cfg.kind == "oneshot" and cfg.max_loops > 0:
            movie = self._current_movie
            if movie:
                current_frame = movie.currentFrameNumber()
                # 检测是否完成一轮（帧号从大变小，说明循环了）
                if self._last_frame_num > 0 and current_frame < self._last_frame_num:
                    self._loop_count += 1
                    if self._loop_count >= cfg.max_loops:
                        # 停止动画，回退到 next
                        movie.stop()
                        fallback = self.scheduler.select("fallback")
                        if fallback:
                            self._play(fallback)
                        return
                self._last_frame_num = current_frame

    def _on_movie_finished(self):
        """QMovie finished 信号回调（oneshot 动作播放完成）"""
        fallback = self.scheduler.select("fallback")
        if fallback:
            self._play(fallback)

    def _on_loop_timeout(self):
        """loop 动作超时，回退到 stay"""
        if self.scheduler.current != "stay":
            print(f"[Info] loop 动作 '{self.scheduler.current}' 超时，回退到 stay")
            self._play("stay")

    def _move_window(self, speed: int):
        """移动窗口（走路时）"""
        screen = QApplication.primaryScreen().geometry()
        pos = self.pos()
        new_x = pos.x() + speed * self._move_direction

        # 到达边界时转向
        if new_x <= 0:
            new_x = 0
            self._move_direction = 1
        elif new_x + self.width() >= screen.width():
            new_x = screen.width() - self.width()
            self._move_direction = -1

        self.move(new_x, pos.y())

    def _on_idle(self):
        """空闲定时器回调"""
        # 只在 stay 状态下触发 idle 动作
        if self.scheduler.current != "stay":
            return
        name = self.scheduler.select("idle")
        if name:
            self._play(name)

    def paintEvent(self, event):
        """绘制当前帧"""
        painter = QPainter(self)
        if self._current_movie:
            pixmap = self._current_movie.currentPixmap()

            # 检测角落颜色作为背景色，创建遮罩使其透明
            img = pixmap.toImage()
            bg_color = img.pixelColor(0, 0)

            # 创建遮罩，把背景色变透明
            mask = pixmap.createMaskFromColor(bg_color, Qt.MaskInColor)
            pixmap.setMask(mask)

            # 走路时根据方向翻转图像
            cfg = self.registry.get(self.scheduler.current)
            if cfg and cfg.move_speed > 0 and self._move_direction < 0:
                transform = QTransform()
                transform.scale(-1, 1)
                pixmap = pixmap.transformed(transform)
                mask = pixmap.mask()

            painter.drawPixmap(0, 0, pixmap)
            self.setMask(mask)

    def mousePressEvent(self, event):
        """鼠标点击"""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        elif event.button() == Qt.RightButton:
            self._show_menu(event.pos())

    def mouseMoveEvent(self, event):
        """鼠标移动（拖拽）"""
        if self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        self._drag_pos = None
        self.setCursor(QCursor(Qt.ArrowCursor))

    def _show_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)

        # 从配置动态生成菜单
        menu_actions = self.registry.get_menu_actions()
        for cfg in menu_actions:
            # 添加当前动作标记
            label = f"• {cfg.label}" if cfg.name == self.scheduler.current else cfg.label
            action = menu.addAction(label)
            action.triggered.connect(lambda checked, n=cfg.name: self._on_menu_click(n))

        menu.addSeparator()
        exit_action = menu.addAction("❌ 退出")
        exit_action.triggered.connect(self.close)

        menu.exec_(self.mapToGlobal(pos))

    def _on_menu_click(self, name: str):
        """菜单点击"""
        selected = self.scheduler.select("menu", name)
        if selected:
            self._play(selected)
