/**
 * Loki Core - 状态机与猫的逻辑
 * 银色虎斑缅因猫像素数据与行为控制
 */

// 像素配色方案
export const COLORS = {
    ' ': null,         // 空白 (透明)
    '#': '#1a1a1a',    // 深色描边
    'G': '#3d3d3d',    // 虎斑纹深
    'g': '#6a6a6a',    // 主毛发灰
    'L': '#8a8a8a',    // 浅灰高光
    'w': '#e8e8e8',    // 白色围脖
    'W': '#f5f5f5',    // 纯白
    'e': '#2e8b57',    // 深绿眼
    'E': '#5fda8a',    // 亮绿眼
    'p': '#ddb8b8',    // 粉鼻
    'P': '#c4a0a0',    // 深粉耳内
    'Y': '#f0e68c',    // 耳毛尖
};

// 像素帧数据
export const FRAMES = {
    sitting: [
        "    #Y     Y#     ",
        "   #P#     #P#    ",
        "   #gg#####gg#    ",
        "  #ggwe#g#g#ewgg# ",
        "  #gwwwwgwgwwwwg# ",
        "  #ggwwgpgpwwgg#  ",
        "   #gggwwwwggg#   ",
        "   #GggwwwwwggG#  ",
        "  #ggGggwwwggGgg# ",
        "  #ggggggggggggg# ",
        "   #ggggggggggg#  ",
        "    #ggggggggg#   ",
        "     #ggggggg#    ",
        "      ##  ##      ",
        "                  ",
        "                  "
    ],
    walking_1: [
        "    #Y     Y#     ",
        "   #P#     #P#    ",
        "   #gg#####gg#    ",
        "  #ggwe#g#g#ewgg# ",
        "  #gwwwwgwgwwwwg# ",
        "  #ggwwgpgpwwgg#  ",
        "   #gggwwwwggg#   ",
        "   #GggwwwwwggG#  ",
        "  #ggGggwwwggGgg# ",
        "  #ggggggggggggg# ",
        "   #ggggggggggg#  ",
        "   #ggggggggggg#  ",
        "  gg#      #gggg  ",
        "  #gg#    #gggg#  ",
        "  ###      ####   ",
        "                  "
    ],
    walking_2: [
        "    #Y     Y#     ",
        "   #P#     #P#    ",
        "   #gg#####gg#    ",
        "  #ggwe#g#g#ewgg# ",
        "  #gwwwwgwgwwwwg# ",
        "  #ggwwgpgpwwgg#  ",
        "   #gggwwwwggg#   ",
        "   #GggwwwwwggG#  ",
        "  #ggGggwwwggGgg# ",
        "  #ggggggggggggg# ",
        "   #ggggggggggg#  ",
        "   #ggggggggggg#  ",
        "   #gggg      #gg ",
        "  #gggg#    #gg#  ",
        "  ####      ###   ",
        "                  "
    ],
    sleeping: [
        "                  ",
        "      ######      ",
        "    ##gggggg##    ",
        "   #ggwwwwwwwgg#  ",
        "  #gggwwwwwwwggg# ",
        "  #ggggwwwwwgggg# ",
        "  #gggggwgwggggg# ",
        "  #gggggpgpggggg# ",
        "  #ggggggggggggg# ",
        "   #############  ",
        "                  ",
        "                  ",
        "                  ",
        "                  ",
        "                  ",
        "                  "
    ],
    yawning: [
        "    #Y     Y#     ",
        "   #P#     #P#    ",
        "   #gg#####gg#    ",
        "  #ggWw#g#g#Wwgg# ",
        "  #gwwwwwwwgwwwg# ",
        "  #ggwwWWpWWwwgg# ",
        "   #gggwwwwggg#   ",
        "   #GggwwwwwggG#  ",
        "  #ggGggwwwggGgg# ",
        "  #ggggggggggggg# ",
        "   #ggggggggggg#  ",
        "    #ggggggggg#   ",
        "     #ggggggg#    ",
        "      ##  ##      ",
        "                  ",
        "                  "
    ]
};

/**
 * Loki 状态机
 */
export class LokiState {
    constructor() {
        this.state = 'sitting';
        this.mode = 'static';  // static | free
        this.walkFrame = 1;
        this.frameCount = 0;

        // 位置与速度
        this.posX = 100;
        this.posY = 100;
        this.speedX = 2;
        this.speedY = 2;

        // 拖拽状态
        this.isDragging = false;
        this.dragOffsetX = 0;
        this.dragOffsetY = 0;

        // 定时器
        this.yawnTimeout = null;
    }

    /**
     * 获取当前帧名称
     */
    getCurrentFrame() {
        if (this.state === 'walking') {
            return `walking_${this.walkFrame}`;
        }
        return this.state;
    }

    /**
     * 设置状态
     */
    setState(newState) {
        this.state = newState;

        if (newState === 'walking') {
            this.walkFrame = 1;
        }

        if (this.yawnTimeout) {
            clearTimeout(this.yawnTimeout);
            this.yawnTimeout = null;
        }
    }

    /**
     * 设置模式
     */
    setMode(mode) {
        this.mode = mode;

        if (mode === 'free') {
            this.setState('walking');
        } else {
            this.setState('sitting');
        }
    }

    /**
     * 播放打哈欠动画
     */
    playYawn(onComplete) {
        this.mode = 'static';
        this.setState('yawning');

        this.yawnTimeout = setTimeout(() => {
            if (this.state === 'yawning') {
                this.setState('sitting');
                if (onComplete) onComplete();
            }
        }, 1500);
    }

    /**
     * 更新行走动画帧
     */
    updateWalkFrame() {
        this.frameCount++;
        if (this.frameCount % 10 === 0) {
            this.walkFrame = this.walkFrame === 1 ? 2 : 1;
        }
    }

    /**
     * 随机化移动速度
     */
    randomizeSpeed() {
        this.speedX = (Math.random() - 0.5) * 4;
        this.speedY = (Math.random() - 0.5) * 4;
    }

    /**
     * 开始拖拽
     */
    startDrag(clientX, clientY) {
        this.isDragging = true;
        this.dragOffsetX = clientX - this.posX;
        this.dragOffsetY = clientY - this.posY;
        this.mode = 'static';
        if (this.state !== 'sleeping') {
            this.setState('sitting');
        }
    }

    /**
     * 拖拽移动
     */
    drag(clientX, clientY) {
        if (this.isDragging) {
            this.posX = clientX - this.dragOffsetX;
            this.posY = clientY - this.dragOffsetY;
        }
    }

    /**
     * 结束拖拽
     */
    endDrag() {
        this.isDragging = false;
    }

    /**
     * 自由移动
     */
    move(canvasWidth, canvasHeight, windowWidth, windowHeight) {
        if (this.mode === 'free' && !this.isDragging) {
            this.posX += this.speedX;
            this.posY += this.speedY;

            // 边界检测
            if (this.posX <= 0 || this.posX + canvasWidth >= windowWidth) {
                this.speedX *= -1;
            }
            if (this.posY <= 0 || this.posY + canvasHeight >= windowHeight) {
                this.speedY *= -1;
            }

            this.updateWalkFrame();
        }
    }
}
