/**
 * Loki 主入口
 * 初始化状态机、渲染器、事件绑定
 */

import { LokiState } from './loki-core.js';
import { LokiRender } from './loki-render.js';

// 全局实例
let state;
let render;
let menu;

/**
 * 初始化
 */
function init() {
    state = new LokiState();
    render = new LokiRender('catCanvas');
    menu = document.getElementById('menu');

    // 初始绘制
    render.draw(state.getCurrentFrame());
    render.setPosition(state.posX, state.posY);

    // 绑定事件
    bindEvents();

    // 启动动画循环
    gameLoop();

    // 定时随机方向
    setInterval(() => {
        if (state.mode === 'free') {
            state.randomizeSpeed();
        }
    }, 3000);
}

/**
 * 绑定事件
 */
function bindEvents() {
    const canvas = render.canvas;

    // 左键拖拽
    canvas.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        state.startDrag(e.clientX, e.clientY);
        render.setCursor('grabbing');
        menu.style.display = 'none';
    });

    // 鼠标移动
    document.addEventListener('mousemove', (e) => {
        if (state.isDragging) {
            state.drag(e.clientX, e.clientY);
            render.setPosition(state.posX, state.posY);
        }
    });

    // 鼠标释放
    document.addEventListener('mouseup', () => {
        if (state.isDragging) {
            state.endDrag();
            render.setCursor(state.state === 'sleeping' ? 'help' : 'grab');
        }
    });

    // 右键菜单
    canvas.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        menu.style.display = 'block';
        menu.style.left = e.clientX + 'px';
        menu.style.top = e.clientY + 'px';
    });

    // 点击其他区域关闭菜单
    document.addEventListener('click', (e) => {
        if (e.target !== canvas && !menu.contains(e.target)) {
            menu.style.display = 'none';
        }
    });
}

/**
 * 游戏循环
 */
function gameLoop() {
    const size = render.getSize();

    state.move(size.width, size.height, window.innerWidth, window.innerHeight);

    // 更新位置和渲染
    render.setPosition(state.posX, state.posY);

    if (state.state === 'walking') {
        render.draw(state.getCurrentFrame());
    }

    requestAnimationFrame(gameLoop);
}

/**
 * 设置状态 (供 HTML 调用)
 */
window.setState = function(newState) {
    state.setState(newState);
    render.draw(state.getCurrentFrame());
    render.setCursor(newState === 'sleeping' ? 'help' : 'grab');
};

/**
 * 设置模式 (供 HTML 调用)
 */
window.setMode = function(mode) {
    state.setMode(mode);
    render.draw(state.getCurrentFrame());
    menu.style.display = 'none';
};

/**
 * 播放打哈欠 (供 HTML 调用)
 */
window.playYawn = function() {
    state.playYawn(() => {
        render.draw(state.getCurrentFrame());
    });
    render.draw('yawning');
};

// DOM 加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
