"""
Loki 像素猫桌面宠物 - Python + tkinter
原生 Canvas 绘制，透明窗口
模块化部件 + 眨眼/耳朵抖动动画
"""

import tkinter as tk
import random

# ============ 像素配色 ============

COLORS = {
    ' ': None,
    '#': '#1a1a1a',
    'G': '#3d3d3d',
    'g': '#6a6a6a',
    'L': '#8a8a8a',
    'w': '#e8e8e8',
    'W': '#f5f5f5',
    'e': '#2e8b57',
    'E': '#5fda8a',
    'p': '#ddb8b8',
    'P': '#c4a0a0',
    'Y': '#f0e68c',
}


# ============ 模块化部件数据 ============

# --- 身体轮廓 ---
OUTLINE = {}
OUTLINE['sitting'] = [
    (11, 1, '#'),
    (6, 2, '#'), (7, 2, '#'), (8, 2, '#'), (9, 2, '#'), (10, 2, '#'),
    (2, 3, '#'), (9, 3, '#'), (16, 3, '#'),
    (2, 4, '#'), (16, 4, '#'),
    (2, 5, '#'), (15, 5, '#'),
    (3, 6, '#'), (14, 6, '#'),
    (3, 7, '#'), (15, 7, '#'),
    (2, 8, '#'), (16, 8, '#'),
    (2, 9, '#'), (16, 9, '#'),
    (3, 10, '#'), (15, 10, '#'),
    (4, 11, '#'), (14, 11, '#'),
]
OUTLINE['walking_1'] = [
    (11, 1, '#'),
    (6, 2, '#'), (7, 2, '#'), (8, 2, '#'), (9, 2, '#'), (10, 2, '#'),
    (2, 3, '#'), (9, 3, '#'), (16, 3, '#'),
    (2, 4, '#'), (16, 4, '#'),
    (2, 5, '#'), (15, 5, '#'),
    (3, 6, '#'), (14, 6, '#'),
    (3, 7, '#'), (15, 7, '#'),
    (2, 8, '#'), (16, 8, '#'),
    (2, 9, '#'), (16, 9, '#'),
    (3, 10, '#'), (15, 10, '#'),
    (3, 11, '#'), (15, 11, '#'),
]
OUTLINE['walking_2'] = OUTLINE['walking_1']
OUTLINE['sleeping'] = [
    (6, 1, '#'), (7, 1, '#'), (8, 1, '#'), (9, 1, '#'), (10, 1, '#'), (11, 1, '#'),
    (4, 2, '#'), (5, 2, '#'), (12, 2, '#'), (13, 2, '#'),
    (3, 3, '#'), (15, 3, '#'),
    (2, 4, '#'), (16, 4, '#'),
    (2, 5, '#'), (16, 5, '#'),
    (2, 6, '#'), (16, 6, '#'),
    (2, 7, '#'), (16, 7, '#'),
    (2, 8, '#'), (16, 8, '#'),
    (3, 9, '#'), (4, 9, '#'), (5, 9, '#'), (6, 9, '#'), (7, 9, '#'), (8, 9, '#'),
    (9, 9, '#'), (10, 9, '#'), (11, 9, '#'), (12, 9, '#'), (13, 9, '#'), (14, 9, '#'), (15, 9, '#'),
]
OUTLINE['yawning'] = OUTLINE['sitting']

# --- 身体主体 ---
BODY = {}
BODY['sitting'] = [
    (3, 3, 'g'), (4, 3, 'g'), (14, 3, 'g'), (15, 3, 'g'),
    (3, 4, 'g'), (15, 4, 'g'),
    (3, 5, 'g'), (4, 5, 'g'), (13, 5, 'g'), (14, 5, 'g'),
    (4, 6, 'g'), (5, 6, 'g'), (6, 6, 'g'), (11, 6, 'g'), (12, 6, 'g'), (13, 6, 'g'),
    (5, 7, 'g'), (6, 7, 'g'), (12, 7, 'g'), (13, 7, 'g'),
    (3, 8, 'g'), (4, 8, 'g'), (6, 8, 'g'), (11, 8, 'g'), (12, 8, 'g'), (14, 8, 'g'), (15, 8, 'g'),
    (3, 9, 'g'), (4, 9, 'g'), (5, 9, 'g'), (6, 9, 'g'), (7, 9, 'g'), (8, 9, 'g'), (9, 9, 'g'),
    (10, 9, 'g'), (11, 9, 'g'), (12, 9, 'g'), (13, 9, 'g'), (14, 9, 'g'), (15, 9, 'g'),
    (4, 10, 'g'), (5, 10, 'g'), (6, 10, 'g'), (7, 10, 'g'), (8, 10, 'g'), (9, 10, 'g'),
    (10, 10, 'g'), (11, 10, 'g'), (12, 10, 'g'), (13, 10, 'g'), (14, 10, 'g'),
    (5, 11, 'g'), (6, 11, 'g'), (7, 11, 'g'), (8, 11, 'g'), (9, 11, 'g'),
    (10, 11, 'g'), (11, 11, 'g'), (12, 11, 'g'), (13, 11, 'g'),
]
BODY['walking_1'] = [
    (3, 3, 'g'), (4, 3, 'g'), (14, 3, 'g'), (15, 3, 'g'),
    (3, 4, 'g'), (15, 4, 'g'),
    (3, 5, 'g'), (4, 5, 'g'), (13, 5, 'g'), (14, 5, 'g'),
    (4, 6, 'g'), (5, 6, 'g'), (6, 6, 'g'), (11, 6, 'g'), (12, 6, 'g'), (13, 6, 'g'),
    (5, 7, 'g'), (6, 7, 'g'), (12, 7, 'g'), (13, 7, 'g'),
    (3, 8, 'g'), (4, 8, 'g'), (6, 8, 'g'), (11, 8, 'g'), (12, 8, 'g'), (14, 8, 'g'), (15, 8, 'g'),
    (3, 9, 'g'), (4, 9, 'g'), (5, 9, 'g'), (6, 9, 'g'), (7, 9, 'g'), (8, 9, 'g'), (9, 9, 'g'),
    (10, 9, 'g'), (11, 9, 'g'), (12, 9, 'g'), (13, 9, 'g'), (14, 9, 'g'), (15, 9, 'g'),
    (4, 10, 'g'), (5, 10, 'g'), (6, 10, 'g'), (7, 10, 'g'), (8, 10, 'g'), (9, 10, 'g'),
    (10, 10, 'g'), (11, 10, 'g'), (12, 10, 'g'), (13, 10, 'g'), (14, 10, 'g'),
    (4, 11, 'g'), (5, 11, 'g'), (6, 11, 'g'), (7, 11, 'g'), (8, 11, 'g'), (9, 11, 'g'),
    (10, 11, 'g'), (11, 11, 'g'), (12, 11, 'g'), (13, 11, 'g'), (14, 11, 'g'),
]
BODY['walking_2'] = BODY['walking_1']
BODY['sleeping'] = [
    (6, 2, 'g'), (7, 2, 'g'), (8, 2, 'g'), (9, 2, 'g'), (10, 2, 'g'), (11, 2, 'g'),
    (4, 3, 'g'), (5, 3, 'g'), (13, 3, 'g'), (14, 3, 'g'),
    (3, 4, 'g'), (4, 4, 'g'), (5, 4, 'g'), (13, 4, 'g'), (14, 4, 'g'), (15, 4, 'g'),
    (3, 5, 'g'), (4, 5, 'g'), (5, 5, 'g'), (6, 5, 'g'), (12, 5, 'g'), (13, 5, 'g'), (14, 5, 'g'), (15, 5, 'g'),
    (3, 6, 'g'), (4, 6, 'g'), (5, 6, 'g'), (6, 6, 'g'), (7, 6, 'g'), (9, 6, 'g'),
    (11, 6, 'g'), (12, 6, 'g'), (13, 6, 'g'), (14, 6, 'g'), (15, 6, 'g'),
    (3, 7, 'g'), (4, 7, 'g'), (5, 7, 'g'), (6, 7, 'g'), (7, 7, 'g'), (9, 7, 'g'),
    (11, 7, 'g'), (12, 7, 'g'), (13, 7, 'g'), (14, 7, 'g'), (15, 7, 'g'),
    (3, 8, 'g'), (4, 8, 'g'), (5, 8, 'g'), (6, 8, 'g'), (7, 8, 'g'), (8, 8, 'g'), (9, 8, 'g'),
    (10, 8, 'g'), (11, 8, 'g'), (12, 8, 'g'), (13, 8, 'g'), (14, 8, 'g'), (15, 8, 'g'),
]
BODY['yawning'] = BODY['sitting']

# --- 虎斑纹 ---
BODY_STRIPE = {}
BODY_STRIPE['sitting'] = [(4, 7, 'G'), (14, 7, 'G'), (5, 8, 'G'), (13, 8, 'G')]
BODY_STRIPE['walking_1'] = [(4, 7, 'G'), (14, 7, 'G'), (5, 8, 'G'), (13, 8, 'G')]
BODY_STRIPE['walking_2'] = BODY_STRIPE['walking_1']
BODY_STRIPE['sleeping'] = []
BODY_STRIPE['yawning'] = BODY_STRIPE['sitting']

# --- 围脖/胸部 ---
CHEST = {}
CHEST['sitting'] = [
    (8, 3, 'g'), (4, 4, 'w'), (8, 4, 'g'), (9, 4, 'w'), (14, 4, 'w'),
    (5, 5, 'w'), (6, 5, 'w'), (7, 5, 'g'), (11, 5, 'w'), (12, 5, 'w'),
    (7, 6, 'w'), (8, 6, 'w'), (9, 6, 'w'), (10, 6, 'w'),
    (7, 7, 'w'), (8, 7, 'w'), (9, 7, 'w'), (10, 7, 'w'), (11, 7, 'w'),
    (7, 8, 'g'), (8, 8, 'w'), (9, 8, 'w'), (10, 8, 'w'),
]
CHEST['walking_1'] = CHEST['sitting']
CHEST['walking_2'] = CHEST['sitting']
CHEST['sleeping'] = [
    (6, 3, 'w'), (7, 3, 'w'), (8, 3, 'w'), (9, 3, 'w'), (10, 3, 'w'), (11, 3, 'w'), (12, 3, 'w'),
    (6, 4, 'w'), (7, 4, 'w'), (8, 4, 'w'), (9, 4, 'w'), (10, 4, 'w'), (11, 4, 'w'), (12, 4, 'w'),
    (7, 5, 'w'), (8, 5, 'w'), (9, 5, 'w'), (10, 5, 'w'), (11, 5, 'w'),
    (8, 6, 'w'), (10, 6, 'w'),
]
CHEST['yawning'] = [
    (8, 3, 'g'), (4, 4, 'w'), (8, 4, 'w'), (9, 4, 'w'), (14, 4, 'w'),
    (5, 5, 'w'), (6, 5, 'w'), (7, 5, 'W'), (11, 5, 'W'), (12, 5, 'w'), (13, 5, 'w'),
    (7, 6, 'w'), (8, 6, 'w'), (9, 6, 'w'), (10, 6, 'w'),
    (7, 7, 'w'), (8, 7, 'w'), (9, 7, 'w'), (10, 7, 'w'), (11, 7, 'w'),
    (7, 8, 'g'), (8, 8, 'w'), (9, 8, 'w'), (10, 8, 'w'),
]

# --- 尾巴 ---
TAIL = {}
TAIL['sitting'] = [
    (17, 5, '#'),
    (17, 6, 'g'), (18, 6, '#'),
    (16, 7, 'g'), (17, 7, 'g'), (18, 7, '#'),
    (16, 8, 'g'), (17, 8, '#'),
    (16, 9, 'g'), (17, 9, '#'),
]
TAIL['walking_1'] = [
    (15, 4, '#'),
    (15, 5, 'g'), (16, 5, '#'),
    (14, 6, 'g'), (15, 6, 'g'), (16, 6, '#'),
    (14, 7, 'g'), (15, 7, '#'),
    (14, 8, 'g'), (15, 8, '#'),
]
TAIL['walking_2'] = [
    (17, 4, '#'),
    (17, 5, 'g'), (18, 5, '#'),
    (17, 6, 'g'), (18, 6, 'g'), (19, 6, '#'),
    (17, 7, 'g'), (18, 7, '#'),
    (17, 8, 'g'), (18, 8, '#'),
]
TAIL['sleeping'] = [
    (3, 7, 'g'), (2, 7, 'g'),
    (3, 8, 'g'), (2, 8, 'g'),
]
TAIL['yawning'] = TAIL['sitting']

# --- 前脚 ---
LEGS = {}
LEGS['sitting'] = [
    (5, 12, '#'), (6, 12, 'g'), (7, 12, 'g'), (8, 12, 'g'), (9, 12, 'g'), (10, 12, 'g'), (11, 12, 'g'), (12, 12, 'g'), (13, 12, '#'),
    (5, 13, '#'), (6, 13, 'g'), (7, 13, 'g'), (10, 13, 'g'), (11, 13, 'g'), (12, 13, '#'),
    (6, 14, '#'), (7, 14, '#'), (10, 14, '#'), (11, 14, '#'),
]
LEGS['walking_1'] = [
    (3, 12, '#'), (4, 12, 'g'), (5, 12, 'g'), (6, 12, '#'),
    (11, 12, '#'), (12, 12, 'g'), (13, 12, 'g'), (14, 12, '#'),
    (3, 13, '#'), (4, 13, 'g'), (5, 13, '#'),
    (11, 13, '#'), (12, 13, 'g'), (13, 13, '#'),
    (3, 14, '#'), (4, 14, '#'),
    (11, 14, '#'), (12, 14, '#'),
]
LEGS['walking_2'] = [
    (5, 12, '#'), (6, 12, 'g'), (7, 12, 'g'), (8, 12, '#'),
    (12, 12, '#'), (13, 12, 'g'), (14, 12, 'g'), (15, 12, '#'),
    (5, 13, '#'), (6, 13, 'g'), (7, 13, '#'),
    (12, 13, '#'), (13, 13, 'g'), (14, 13, '#'),
    (5, 14, '#'), (6, 14, '#'),
    (12, 14, '#'), (13, 14, '#'),
]
LEGS['sleeping'] = []
LEGS['yawning'] = LEGS['sitting']

# --- 左耳 ---
EAR_LEFT = {}
EAR_LEFT['sitting'] = [
    (4, 0, '#'), (5, 0, 'Y'),
    (3, 1, '#'), (4, 1, 'P'), (5, 1, '#'),
    (3, 2, '#'), (4, 2, 'g'), (5, 2, 'g'),
]
EAR_LEFT['walking_1'] = EAR_LEFT['sitting']
EAR_LEFT['walking_2'] = EAR_LEFT['sitting']
EAR_LEFT['sleeping'] = []
EAR_LEFT['yawning'] = EAR_LEFT['sitting']
EAR_LEFT['twitch'] = [  # 耳朵抖动
    (4, 0, '#'), (5, 0, 'Y'), (6, 0, '#'),
    (4, 1, 'P'), (5, 1, '#'), (6, 1, '#'),
    (3, 2, '#'), (4, 2, 'g'), (5, 2, 'g'),
]

# --- 右耳 ---
EAR_RIGHT = {}
EAR_RIGHT['sitting'] = [
    (11, 0, 'Y'), (12, 0, '#'), (13, 0, '#'),
    (12, 1, 'P'), (13, 1, '#'),
    (11, 2, 'g'), (12, 2, 'g'), (13, 2, '#'),
]
EAR_RIGHT['walking_1'] = EAR_RIGHT['sitting']
EAR_RIGHT['walking_2'] = EAR_RIGHT['sitting']
EAR_RIGHT['sleeping'] = []
EAR_RIGHT['yawning'] = EAR_RIGHT['sitting']
EAR_RIGHT['twitch'] = [  # 耳朵抖动
    (10, 0, '#'), (11, 0, 'Y'), (12, 0, '#'),
    (11, 1, '#'), (12, 1, 'P'), (13, 1, '#'),
    (11, 2, 'g'), (12, 2, 'g'), (13, 2, '#'),
]

# --- 左眼 ---
EYE_LEFT = {}
EYE_LEFT['sitting'] = [
    (5, 3, 'w'), (6, 3, 'e'), (7, 3, '#'),
    (5, 4, 'w'), (6, 4, 'w'), (7, 4, 'w'),
]
EYE_LEFT['walking_1'] = EYE_LEFT['sitting']
EYE_LEFT['walking_2'] = EYE_LEFT['sitting']
EYE_LEFT['sleeping'] = []
EYE_LEFT['yawning'] = [
    (5, 3, 'W'), (6, 3, 'w'), (7, 3, '#'),
    (5, 4, 'w'), (6, 4, 'w'), (7, 4, 'w'),
]
EYE_LEFT['blink'] = [  # 眨眼（闭眼）
    (5, 3, 'w'), (6, 3, 'w'), (7, 3, '#'),
    (5, 4, 'w'), (6, 4, 'w'), (7, 4, 'w'),
]

# --- 右眼 ---
EYE_RIGHT = {}
EYE_RIGHT['sitting'] = [
    (10, 3, 'g'), (11, 3, '#'), (12, 3, 'e'), (13, 3, 'w'),
    (10, 4, 'g'), (11, 4, 'w'), (12, 4, 'w'), (13, 4, 'w'),
]
EYE_RIGHT['walking_1'] = EYE_RIGHT['sitting']
EYE_RIGHT['walking_2'] = EYE_RIGHT['sitting']
EYE_RIGHT['sleeping'] = []
EYE_RIGHT['yawning'] = [
    (10, 3, 'g'), (11, 3, '#'), (12, 3, 'W'), (13, 3, 'w'),
    (10, 4, 'w'), (11, 4, 'g'), (12, 4, 'w'), (13, 4, 'w'),
]
EYE_RIGHT['blink'] = [  # 眨眼（闭眼）
    (10, 3, 'g'), (11, 3, '#'), (12, 3, 'w'), (13, 3, 'w'),
    (10, 4, 'g'), (11, 4, 'w'), (12, 4, 'w'), (13, 4, 'w'),
]

# --- 鼻子 ---
NOSE = {}
NOSE['sitting'] = [(8, 5, 'p'), (9, 5, 'g'), (10, 5, 'p')]
NOSE['walking_1'] = NOSE['sitting']
NOSE['walking_2'] = NOSE['sitting']
NOSE['sleeping'] = [(8, 7, 'p'), (10, 7, 'p')]
NOSE['yawning'] = [(8, 5, 'W'), (9, 5, 'p'), (10, 5, 'W')]


class LokiPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loki")

        # 窗口属性
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', '#010101')
        self.root.configure(bg='#010101')

        # 窗口尺寸
        self.width = 300
        self.height = 260
        self.pixel_size = 12
        self.offset_x = 30

        # 定位到右下角
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.pos_x = screen_w - self.width - 50
        self.pos_y = screen_h - self.height - 100
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg='#010101',
            highlightthickness=0
        )
        self.canvas.pack()

        # 状态
        self.state = 'sitting'
        self.mode = 'static'
        self.walk_frame = 1
        self.frame_count = 0
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])
        self.yawn_after_id = None

        # 眨眼和耳朵抖动状态
        self.is_blinking = False
        self.is_ear_twitching = False
        self.ear_side = 'left'

        # 拖拽
        self.drag_start_x = 0
        self.drag_start_y = 0

        # 右键菜单
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="😴 睡觉", command=lambda: self.set_state('sleeping'))
        self.menu.add_command(label="🥱 打哈欠", command=self.play_yawn)
        self.menu.add_separator()
        self.menu.add_command(label="🛑 静态模式", command=lambda: self.set_mode('static'))
        self.menu.add_command(label="🐾 自由移动", command=lambda: self.set_mode('free'))
        self.menu.add_separator()
        self.menu.add_command(label="❌ 退出", command=self.root.quit)

        # 绑定事件
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<Button-3>', self.on_right_click)

        # 初始绘制
        self.draw_cat(self.state)

        # 启动动画
        self.animate()
        self.random_direction()
        self.schedule_blink()
        self.schedule_ear_twitch()

        # 托盘
        self.setup_tray()

    def draw_pixel(self, x, y, char):
        """绘制单个像素块"""
        color = COLORS.get(char)
        if color:
            self.canvas.create_rectangle(
                x * self.pixel_size + self.offset_x,
                y * self.pixel_size,
                (x + 1) * self.pixel_size + self.offset_x,
                (y + 1) * self.pixel_size,
                fill=color,
                outline=color,
                tags='pixel'
            )

    def draw_part(self, part_data, state):
        """绘制单个部件"""
        pixels = part_data.get(state, part_data.get('sitting', []))
        for pixel in pixels:
            if len(pixel) == 3:
                x, y, char = pixel
                self.draw_pixel(x, y, char)

    def draw_cat_modular(self, state):
        """模块化绘制：按部件层叠渲染"""
        self.canvas.delete('all')

        # 渲染顺序（从底到顶）
        self.draw_part(BODY, state)
        self.draw_part(OUTLINE, state)
        self.draw_part(BODY_STRIPE, state)
        self.draw_part(CHEST, state)
        self.draw_part(TAIL, state)
        self.draw_part(LEGS, state)

        # 眼睛（支持眨眼）
        eye_state = 'blink' if self.is_blinking else state
        if eye_state not in EYE_LEFT:
            eye_state = 'sitting'
        self.draw_part(EYE_LEFT, eye_state)
        self.draw_part(EYE_RIGHT, eye_state)

        self.draw_part(NOSE, state)

        # 耳朵（支持抖动）
        ear_left_state = 'twitch' if (self.is_ear_twitching and self.ear_side == 'left') else state
        ear_right_state = 'twitch' if (self.is_ear_twitching and self.ear_side == 'right') else state
        if ear_left_state not in EAR_LEFT:
            ear_left_state = 'sitting'
        if ear_right_state not in EAR_RIGHT:
            ear_right_state = 'sitting'
        self.draw_part(EAR_LEFT, ear_left_state)
        self.draw_part(EAR_RIGHT, ear_right_state)

    def draw_cat(self, frame_name):
        """绘制像素猫（使用模块化渲染）"""
        self.draw_cat_modular(frame_name)

    def set_state(self, state):
        self.state = state
        if state == 'walking':
            self.walk_frame = 1
            self.draw_cat('walking_1')
        else:
            self.draw_cat(state)

        if self.yawn_after_id:
            self.root.after_cancel(self.yawn_after_id)
            self.yawn_after_id = None

    def set_mode(self, mode):
        self.mode = mode
        if mode == 'free':
            # 重新初始化速度，确保有足够的移动速度
            self.speed_x = random.choice([-3, -2, 2, 3])
            self.speed_y = random.choice([-3, -2, 2, 3])
            self.set_state('walking')
        else:
            self.set_state('sitting')

    def play_yawn(self):
        self.mode = 'static'
        self.set_state('yawning')
        self.yawn_after_id = self.root.after(1500, self._end_yawn)

    def _end_yawn(self):
        if self.state == 'yawning':
            self.set_state('sitting')

    def animate(self):
        """动画循环"""
        if self.mode == 'free' and self.state != 'sleeping':
            self.pos_x += self.speed_x
            self.pos_y += self.speed_y

            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()

            if self.pos_x <= 0 or self.pos_x + self.width >= screen_w:
                self.speed_x *= -1
                self.pos_x = max(0, min(self.pos_x, screen_w - self.width))
            if self.pos_y <= 0 or self.pos_y + self.height >= screen_h - 50:
                self.speed_y *= -1
                self.pos_y = max(0, min(self.pos_y, screen_h - self.height - 50))

            self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

            self.frame_count += 1
            if self.frame_count % 10 == 0:
                self.walk_frame = 2 if self.walk_frame == 1 else 1
                self.draw_cat(f'walking_{self.walk_frame}')

        self.root.after(33, self.animate)

    def random_direction(self):
        if self.mode == 'free':
            # 确保速度有最小绝对值，避免几乎不动的情况
            self.speed_x = (random.random() - 0.5) * 4
            self.speed_y = (random.random() - 0.5) * 4
            # 如果速度太小，重新设置
            if abs(self.speed_x) < 1:
                self.speed_x = random.choice([-2, 2])
            if abs(self.speed_y) < 1:
                self.speed_y = random.choice([-2, 2])
        self.root.after(3000, self.random_direction)

    def on_left_click(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.mode = 'static'
        if self.state != 'sleeping':
            self.set_state('sitting')

    def on_drag(self, event):
        self.pos_x = self.root.winfo_x() + event.x - self.drag_start_x
        self.pos_y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

    def on_right_click(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def setup_tray(self):
        try:
            import pystray
            from PIL import Image, ImageDraw

            def create_icon():
                img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.ellipse([20, 15, 44, 45], fill='#6a6a6a', outline='#1a1a1a')
                draw.polygon([16, 18, 24, 8, 28, 18], fill='#6a6a6a', outline='#1a1a1a')
                draw.polygon([48, 18, 40, 8, 36, 18], fill='#6a6a6a', outline='#1a1a1a')
                draw.ellipse([26, 25, 30, 29], fill='#2e8b57')
                draw.ellipse([34, 25, 38, 29], fill='#2e8b57')
                return img

            def on_exit(icon, item):
                icon.stop()
                self.root.quit()

            def on_show(icon, item):
                self.root.deiconify()

            menu = pystray.Menu(
                pystray.MenuItem("显示", on_show),
                pystray.MenuItem("退出", on_exit)
            )

            self.icon = pystray.Icon("loki", create_icon(), "Loki 桌宠", menu)
            self.icon.run_detached()

        except ImportError:
            pass

    def schedule_blink(self):
        if self.state != 'sleeping':
            delay = random.randint(2000, 5000)
            self.root.after(delay, self.do_blink)
        else:
            self.root.after(3000, self.schedule_blink)

    def do_blink(self):
        if self.state == 'sleeping':
            self.schedule_blink()
            return
        self.is_blinking = True
        # 使用正确的帧名
        frame = f'walking_{self.walk_frame}' if self.state == 'walking' else self.state
        self.draw_cat(frame)
        self.root.after(150, self.end_blink)

    def end_blink(self):
        self.is_blinking = False
        frame = f'walking_{self.walk_frame}' if self.state == 'walking' else self.state
        self.draw_cat(frame)
        self.schedule_blink()

    def schedule_ear_twitch(self):
        if self.state != 'sleeping':
            delay = random.randint(3000, 8000)
            self.root.after(delay, self.do_ear_twitch)
        else:
            self.root.after(5000, self.schedule_ear_twitch)

    def do_ear_twitch(self):
        if self.state == 'sleeping':
            self.schedule_ear_twitch()
            return
        self.ear_side = random.choice(['left', 'right'])
        self.is_ear_twitching = True
        frame = f'walking_{self.walk_frame}' if self.state == 'walking' else self.state
        self.draw_cat(frame)
        self.root.after(100, self.end_ear_twitch)

    def end_ear_twitch(self):
        self.is_ear_twitching = False
        frame = f'walking_{self.walk_frame}' if self.state == 'walking' else self.state
        self.draw_cat(frame)
        self.schedule_ear_twitch()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pet = LokiPet()
    pet.run()
