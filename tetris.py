import pygame
import random
import time

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 定义游戏区域大小
BLOCK_SIZE = 30  # 每个方块的大小
GRID_WIDTH = 10  # 游戏区域宽度（以方块为单位）
GRID_HEIGHT = 20  # 游戏区域高度（以方块为单位）

# 计算实际窗口大小
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # 额外空间用于显示下一个方块和分数
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 创建时钟对象
clock = pygame.time.Clock()

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# 定义颜色列表（对应每种方块）
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, BLUE, RED, GREEN, RED]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        # 矩阵转置然后反转每一行，实现90度旋转
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows-1-j][i] for j in range(rows)] for i in range(cols)]
        return rotated

class TetrisGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 0.5  # 初始下落速度（秒）

    def new_piece(self):
        # 随机选择一个新的方块
        shape = random.choice(SHAPES)
        # 在屏幕顶部中间位置生成方块
        return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)

    def valid_move(self, piece, x, y, shape=None):
        if shape is None:
            shape = piece.shape
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def draw_grid(self):
        # 绘制游戏区域背景
        pygame.draw.rect(screen, WHITE, (0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 1)
        
        # 绘制网格线
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(screen, GRAY, 
                               (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # 绘制已固定的方块
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(screen, self.grid[i][j],
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_piece(self, piece):
        if piece:
            for i, row in enumerate(piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, piece.color,
                                       ((piece.x + j) * BLOCK_SIZE,
                                        (piece.y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_piece(self):
        # 绘制"下一个方块"区域
        next_piece_x = GRID_WIDTH * BLOCK_SIZE + 20
        next_piece_y = 50
        
        # 绘制标题
        font = pygame.font.Font(None, 36)
        text = font.render("下一个:", True, WHITE)
        screen.blit(text, (next_piece_x, 10))
        
        # 绘制下一个方块
        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece.color,
                                   (next_piece_x + j * BLOCK_SIZE,
                                    next_piece_y + i * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self):
        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        level_text = font.render(f"等级: {self.level}", True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 150))
        screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 20, 190))

def main():
    game = TetrisGame()
    last_move_down_time = time.time()
    move_down_interval = 0.5  # 初始下落间隔（秒）

    running = True
    while running:
        current_time = time.time()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.game_over:
                    # 按空格键重新开始游戏
                    game.reset_game()
                    last_move_down_time = time.time()
                    move_down_interval = 0.5
                elif not game.game_over:
                    if event.key == pygame.K_LEFT:
                        if game.valid_move(game.current_piece, game.current_piece.x - 1, game.current_piece.y):
                            game.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if game.valid_move(game.current_piece, game.current_piece.x + 1, game.current_piece.y):
                            game.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y + 1):
                            game.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        rotated_shape = game.current_piece.rotate()
                        if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y, rotated_shape):
                            game.current_piece.shape = rotated_shape

        # 自动下落
        if current_time - last_move_down_time > move_down_interval and not game.game_over:
            if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y + 1):
                game.current_piece.y += 1
            else:
                # 固定当前方块
                for i, row in enumerate(game.current_piece.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            game.grid[game.current_piece.y + i][game.current_piece.x + j] = game.current_piece.color
                
                # 检查是否有完整的行
                full_rows = []
                for i in range(GRID_HEIGHT):
                    if all(game.grid[i]):
                        full_rows.append(i)
                
                # 消除完整的行并更新分数
                for row in full_rows:
                    del game.grid[row]
                    game.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                    game.score += 100
                    if game.score % 1000 == 0:
                        game.level += 1
                        move_down_interval = max(0.1, 0.5 - (game.level - 1) * 0.05)
                
                # 生成新的方块
                game.current_piece = game.next_piece
                game.next_piece = game.new_piece()
                
                # 检查游戏是否结束
                if not game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y):
                    game.game_over = True
            
            last_move_down_time = current_time
        
        # 绘制游戏界面
        screen.fill(BLACK)
        game.draw_grid()
        game.draw_piece(game.current_piece)
        game.draw_next_piece()
        game.draw_score()
        
        # 如果游戏结束，显示游戏结束文字和重新开始提示
        if game.game_over:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render("游戏结束!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over_text, text_rect)
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("按空格键重新开始", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()
