/**
 * Loki Render - Canvas 渲染器
 * 像素猫绘制与 Canvas 管理
 */

import { COLORS, FRAMES } from './loki-core.js';

export class LokiRender {
    constructor(canvasId, pixelSize = 12, offsetX = 30) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.pixelSize = pixelSize;
        this.offsetX = offsetX;
    }

    /**
     * 绘制指定帧
     */
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

    /**
     * 更新 Canvas 位置
     */
    setPosition(x, y) {
        this.canvas.style.left = x + 'px';
        this.canvas.style.top = y + 'px';
    }

    /**
     * 设置鼠标样式
     */
    setCursor(cursor) {
        this.canvas.style.cursor = cursor;
    }

    /**
     * 获取 Canvas 尺寸
     */
    getSize() {
        return {
            width: this.canvas.width,
            height: this.canvas.height
        };
    }
}
