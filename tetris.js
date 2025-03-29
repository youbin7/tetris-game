const BLOCK_SIZE = 30;
const GRID_WIDTH = 10;
const GRID_HEIGHT = 20;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 设置画布大小
canvas.width = BLOCK_SIZE * (GRID_WIDTH + 8);
canvas.height = BLOCK_SIZE * GRID_HEIGHT;

// 颜色定义
const COLORS = {
    CYAN: '#00FFFF',
    YELLOW: '#FFFF00',
    MAGENTA: '#FF00FF',
    RED: '#FF0000',
    GREEN: '#00FF00',
    BLUE: '#0000FF',
    GRAY: '#808080',
    WHITE: '#FFFFFF',
    BLACK: '#000000'
};

// 方块形状定义
const SHAPES = [
    [[1, 1, 1, 1]],  // I
    [[1, 1], [1, 1]],  // O
    [[1, 1, 1], [0, 1, 0]],  // T
    [[1, 1, 1], [1, 0, 0]],  // L
    [[1, 1, 1], [0, 0, 1]],  // J
    [[1, 1, 0], [0, 1, 1]],  // S
    [[0, 1, 1], [1, 1, 0]]   // Z
];

const SHAPE_COLORS = [COLORS.CYAN, COLORS.YELLOW, COLORS.MAGENTA, COLORS.BLUE, COLORS.RED, COLORS.GREEN, COLORS.RED];

class Tetromino {
    constructor(x, y, shape) {
        this.x = x;
        this.y = y;
        this.shape = shape;
        this.color = SHAPE_COLORS[SHAPES.indexOf(shape)];
    }

    rotate() {
        const rows = this.shape.length;
        const cols = this.shape[0].length;
        const rotated = Array.from({length: cols}, () => Array(rows).fill(0));
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                rotated[j][rows - 1 - i] = this.shape[i][j];
            }
        }
        return rotated;
    }
}

class TetrisGame {
    constructor() {
        this.reset();
    }

    reset() {
        this.grid = Array.from({length: GRID_HEIGHT}, () => Array(GRID_WIDTH).fill(0));
        this.currentPiece = this.newPiece();
        this.nextPiece = this.newPiece();
        this.gameOver = false;
        this.score = 0;
        this.level = 1;
        this.updateScore();
    }

    newPiece() {
        const shape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
        return new Tetromino(Math.floor(GRID_WIDTH / 2) - Math.floor(shape[0].length / 2), 0, shape);
    }

    validMove(piece, x, y, shape = null) {
        const testShape = shape || piece.shape;
        
        for (let i = 0; i < testShape.length; i++) {
            for (let j = 0; j < testShape[i].length; j++) {
                if (testShape[i][j]) {
                    const newX = x + j;
                    const newY = y + i;
                    if (newX < 0 || newX >= GRID_WIDTH || newY >= GRID_HEIGHT ||
                        (newY >= 0 && this.grid[newY][newX])) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    updateScore() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('level').textContent = this.level;
    }

    drawGrid() {
        // 绘制背景
        ctx.fillStyle = COLORS.BLACK;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 绘制网格
        for (let i = 0; i < GRID_HEIGHT; i++) {
            for (let j = 0; j < GRID_WIDTH; j++) {
                ctx.strokeStyle = COLORS.GRAY;
                ctx.strokeRect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                
                if (this.grid[i][j]) {
                    ctx.fillStyle = this.grid[i][j];
                    ctx.fillRect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                }
            }
        }
    }

    drawPiece(piece) {
        if (!piece) return;
        
        ctx.fillStyle = piece.color;
        for (let i = 0; i < piece.shape.length; i++) {
            for (let j = 0; j < piece.shape[i].length; j++) {
                if (piece.shape[i][j]) {
                    ctx.fillRect(
                        (piece.x + j) * BLOCK_SIZE,
                        (piece.y + i) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    );
                }
            }
        }
    }

    drawNextPiece() {
        const nextX = (GRID_WIDTH + 1) * BLOCK_SIZE;
        const nextY = 2 * BLOCK_SIZE;

        // 绘制"下一个"文字
        ctx.fillStyle = COLORS.WHITE;
        ctx.font = '20px Arial';
        ctx.fillText('下一个:', nextX, BLOCK_SIZE);

        // 绘制下一个方块
        for (let i = 0; i < this.nextPiece.shape.length; i++) {
            for (let j = 0; j < this.nextPiece.shape[i].length; j++) {
                if (this.nextPiece.shape[i][j]) {
                    ctx.fillStyle = this.nextPiece.color;
                    ctx.fillRect(
                        nextX + j * BLOCK_SIZE,
                        nextY + i * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    );
                }
            }
        }
    }

    draw() {
        this.drawGrid();
        this.drawPiece(this.currentPiece);
        this.drawNextPiece();

        if (this.gameOver) {
            ctx.fillStyle = COLORS.RED;
            ctx.font = '48px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('游戏结束!', canvas.width / 2, canvas.height / 2);
            
            ctx.fillStyle = COLORS.WHITE;
            ctx.font = '24px Arial';
            ctx.fillText('按空格键重新开始', canvas.width / 2, canvas.height / 2 + 40);
        }
    }
}

const game = new TetrisGame();
let dropInterval = 1000;
let lastDrop = 0;

function update(timestamp) {
    if (!lastDrop) lastDrop = timestamp;
    
    if (!game.gameOver && timestamp - lastDrop > dropInterval) {
        if (game.validMove(game.currentPiece, game.currentPiece.x, game.currentPiece.y + 1)) {
            game.currentPiece.y++;
        } else {
            // 固定当前方块
            for (let i = 0; i < game.currentPiece.shape.length; i++) {
                for (let j = 0; j < game.currentPiece.shape[i].length; j++) {
                    if (game.currentPiece.shape[i][j]) {
                        game.grid[game.currentPiece.y + i][game.currentPiece.x + j] = game.currentPiece.color;
                    }
                }
            }

            // 检查消行
            let linesCleared = 0;
            for (let i = GRID_HEIGHT - 1; i >= 0; i--) {
                if (game.grid[i].every(cell => cell !== 0)) {
                    game.grid.splice(i, 1);
                    game.grid.unshift(Array(GRID_WIDTH).fill(0));
                    linesCleared++;
                    i++;
                }
            }

            // 更新分数
            if (linesCleared > 0) {
                game.score += linesCleared * 100;
                if (game.score >= game.level * 1000) {
                    game.level++;
                    dropInterval = Math.max(100, 1000 - (game.level - 1) * 50);
                }
                game.updateScore();
            }

            // 生成新方块
            game.currentPiece = game.nextPiece;
            game.nextPiece = game.newPiece();

            // 检查游戏是否结束
            if (!game.validMove(game.currentPiece, game.currentPiece.x, game.currentPiece.y)) {
                game.gameOver = true;
            }
        }
        lastDrop = timestamp;
    }

    game.draw();
    requestAnimationFrame(update);
}

// 键盘控制
document.addEventListener('keydown', (event) => {
    if (game.gameOver) {
        if (event.code === 'Space') {
            game.reset();
            dropInterval = 1000;
        }
        return;
    }

    switch (event.code) {
        case 'ArrowLeft':
            if (game.validMove(game.currentPiece, game.currentPiece.x - 1, game.currentPiece.y)) {
                game.currentPiece.x--;
            }
            break;
        case 'ArrowRight':
            if (game.validMove(game.currentPiece, game.currentPiece.x + 1, game.currentPiece.y)) {
                game.currentPiece.x++;
            }
            break;
        case 'ArrowDown':
            if (game.validMove(game.currentPiece, game.currentPiece.x, game.currentPiece.y + 1)) {
                game.currentPiece.y++;
            }
            break;
        case 'ArrowUp':
            const rotated = game.currentPiece.rotate();
            if (game.validMove(game.currentPiece, game.currentPiece.x, game.currentPiece.y, rotated)) {
                game.currentPiece.shape = rotated;
            }
            break;
    }
});

// 开始游戏
requestAnimationFrame(update); 