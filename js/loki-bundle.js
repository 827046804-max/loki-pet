/**
 * Loki Bundle - 合并版本 (可直接在浏览器打开)
 */

// ============ loki-core.js ============

const COLORS = {
    ' ': null,
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
};

const FRAMES = {
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

class LokiState {
    constructor() {
        this.state = 'sitting';
        this.mode = 'static';
        this.walkFrame = 1;
        this.frameCount = 0;
        this.posX = 100;
        this.posY = 100;
        this.speedX = 2;
        this.speedY = 2;
        this.isDragging = false;
        this.dragOffsetX = 0;
        this.dragOffsetY = 0;
        this.yawnTimeout = null;
    }

    getCurrentFrame() {
        if (this.state === 'walking') {
            return `walking_${this.walkFrame}`;
        }
        return this.state;
    }

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

    setMode(mode) {
        this.mode = mode;
        if (mode === 'free') {
            this.setState('walking');
        } else {
            this.setState('sitting');
        }
    }

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

    updateWalkFrame() {
        this.frameCount++;
        if (this.frameCount % 10 === 0) {
            this.walkFrame = this.walkFrame === 1 ? 2 : 1;
        }
    }

    randomizeSpeed() {
        this.speedX = (Math.random() - 0.5) * 4;
        this.speedY = (Math.random() - 0.5) * 4;
    }

    startDrag(clientX, clientY) {
        this.isDragging = true;
        this.dragOffsetX = clientX - this.posX;
        this.dragOffsetY = clientY - this.posY;
        this.mode = 'static';
        if (this.state !== 'sleeping') {
            this.setState('sitting');
        }
    }

    drag(clientX, clientY) {
        if (this.isDragging) {
            this.posX = clientX - this.dragOffsetX;
            this.posY = clientY - this.dragOffsetY;
        }
    }

    endDrag() {
        this.isDragging = false;
    }

    move(canvasWidth, canvasHeight, windowWidth, windowHeight) {
        if (this.mode === 'free' && !this.isDragging) {
            this.posX += this.speedX;
            this.posY += this.speedY;
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

// ============ loki-render.js ============

class LokiRender {
    constructor(canvasId, pixelSize = 12, offsetX = 30) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.pixelSize = pixelSize;
        this.offsetX = offsetX;
    }

    draw(frameName) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        const frame = FRAMES[frameName];
        if (!frame) return;

        for (let y = 0; y < frame.length; y++) {
            for (let x = 0; x < frame[y].length; x++) {
                const char = frame[y][x];
                const color = COLORS[char];
                if (color) {
                    this.ctx.fillStyle = color;
                    this.ctx.fillRect(
                        x * this.pixelSize + this.offsetX,
                        y * this.pixelSize,
                        this.pixelSize,
                        this.pixelSize
                    );
                }
            }
        }
    }

    setPosition(x, y) {
        this.canvas.style.left = x + 'px';
        this.canvas.style.top = y + 'px';
    }

    setCursor(cursor) {
        this.canvas.style.cursor = cursor;
    }

    getSize() {
        return {
            width: this.canvas.width,
            height: this.canvas.height
        };
    }
}

// ============ main.js ============

let state;
let render;
let menu;

function init() {
    state = new LokiState();
    render = new LokiRender('catCanvas');
    menu = document.getElementById('menu');

    render.draw(state.getCurrentFrame());
    render.setPosition(state.posX, state.posY);

    bindEvents();
    gameLoop();

    setInterval(() => {
        if (state.mode === 'free') {
            state.randomizeSpeed();
        }
    }, 3000);
}

function bindEvents() {
    const canvas = render.canvas;

    canvas.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        state.startDrag(e.clientX, e.clientY);
        render.setCursor('grabbing');
        menu.style.display = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (state.isDragging) {
            state.drag(e.clientX, e.clientY);
            render.setPosition(state.posX, state.posY);
        }
    });

    document.addEventListener('mouseup', () => {
        if (state.isDragging) {
            state.endDrag();
            render.setCursor(state.state === 'sleeping' ? 'help' : 'grab');
        }
    });

    canvas.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        menu.style.display = 'block';
        menu.style.left = e.clientX + 'px';
        menu.style.top = e.clientY + 'px';
    });

    document.addEventListener('click', (e) => {
        if (e.target !== canvas && !menu.contains(e.target)) {
            menu.style.display = 'none';
        }
    });
}

function gameLoop() {
    const size = render.getSize();
    state.move(size.width, size.height, window.innerWidth, window.innerHeight);
    render.setPosition(state.posX, state.posY);

    if (state.state === 'walking') {
        render.draw(state.getCurrentFrame());
    }

    requestAnimationFrame(gameLoop);
}

window.setState = function(newState) {
    state.setState(newState);
    render.draw(state.getCurrentFrame());
    render.setCursor(newState === 'sleeping' ? 'help' : 'grab');
};

window.setMode = function(mode) {
    state.setMode(mode);
    render.draw(state.getCurrentFrame());
    menu.style.display = 'none';
};

window.playYawn = function() {
    state.playYawn(() => {
        render.draw(state.getCurrentFrame());
    });
    render.draw('yawning');
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
