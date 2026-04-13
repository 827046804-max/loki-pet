"""
Loki 桌宠测试版 - 状态切换
猫自己在原地"动"（通过不同 GIF 状态），窗口不动
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenu
from PyQt5.QtGui import QMovie, QPainter, QCursor, QPixmap
from PyQt5.QtCore import Qt, QTimer
from pathlib import Path


class LokiTest(QWidget):
    def __init__(self):
        super().__init__()

        # 状态和动画
        self.state = 'play'  # 当前状态
        self.movies = {}     # 加载的动画
        self.current_movie = None

        # 加载图片资源
        self.load_resources()

        # 窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置初始状态（静止）
        self.set_state('stay')

        # 定位到屏幕右下角
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 50
        y = screen.height() - self.height() - 100
        self.move(x, y)

        # 拖拽
        self.drag_pos = None

        self.show()
        print("Loki 测试版已启动！右键切换状态")

    def load_resources(self):
        """加载图片资源"""
        images_dir = Path('images')

        # 静止状态
        stay_path = images_dir / 'loki_stay.gif'
        if stay_path.exists():
            self.movies['stay'] = QMovie(str(stay_path))
            self.movies['stay'].setCacheMode(QMovie.CacheAll)
            print(f"加载静止: {stay_path}")

        # 玩耍状态
        play_path = images_dir / 'loki_play.gif'
        if play_path.exists():
            self.movies['play'] = QMovie(str(play_path))
            self.movies['play'].setCacheMode(QMovie.CacheAll)
            print(f"加载玩耍: {play_path}")

        # 跳跃状态
        jump_path = images_dir / 'loki_jump.gif'
        if jump_path.exists():
            self.movies['jump'] = QMovie(str(jump_path))
            self.movies['jump'].setCacheMode(QMovie.CacheAll)
            print(f"加载跳跃: {jump_path}")

    def set_state(self, state):
        """切换状态"""
        # 停止当前动画
        if self.current_movie:
            self.current_movie.stop()
            try:
                self.current_movie.frameChanged.disconnect(self.update)
            except:
                pass

        self.state = state

        # 获取对应动画
        if state in self.movies:
            self.current_movie = self.movies[state]
        else:
            # 没有对应状态，用 play
            self.current_movie = self.movies.get('play')

        if self.current_movie:
            self.current_movie.frameChanged.connect(self.update)
            self.current_movie.start()

            # 获取尺寸并设置窗口大小
            while self.current_movie.currentPixmap().isNull():
                self.current_movie.jumpToNextFrame()
            size = self.current_movie.currentPixmap().size()
            self.setFixedSize(size)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.current_movie:
            painter.drawPixmap(0, 0, self.current_movie.currentPixmap())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        elif event.button() == Qt.RightButton:
            self.show_menu(event.pos())

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        self.setCursor(QCursor(Qt.ArrowCursor))

    def show_menu(self, pos):
        menu = QMenu(self)

        # 状态切换菜单
        stay_action = menu.addAction("🐱 静止")
        play_action = menu.addAction("🎾 玩耍")
        jump_action = menu.addAction("🦘 跳跃")

        menu.addSeparator()
        exit_action = menu.addAction("❌ 退出")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == stay_action:
            self.set_state('stay')
        elif action == play_action:
            self.set_state('play')
        elif action == jump_action:
            self.set_state('jump')
        elif action == exit_action:
            self.close()

    def closeEvent(self, event):
        if self.current_movie:
            self.current_movie.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loki = LokiTest()
    sys.exit(app.exec_())