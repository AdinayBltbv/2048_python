import pygame
import sys
import random
import os

pygame.init()

WIDTH, HEIGHT = 400, 500
TILE_SIZE = 100
GRID_LEN = 4
FONT = pygame.font.SysFont("comicsans", 40)
BIG_FONT = pygame.font.SysFont("comicsans", 60)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (187, 173, 160)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

grid = [[0] * GRID_LEN for _ in range(GRID_LEN)]
score = 0
best_score = 0

if os.path.exists("best_score.txt"):
    with open("best_score.txt", "r") as f:
        try:
            best_score = int(f.read())
        except:
            best_score = 0

def new_tile():
    r, c = random.choice([(r, c) for r in range(GRID_LEN) for c in range(GRID_LEN) if grid[r][c] == 0])
    grid[r][c] = random.choice([2] * 9 + [4])

def reset_game():
    global grid, score
    grid = [[0] * GRID_LEN for _ in range(GRID_LEN)]
    score = 0
    new_tile()
    new_tile()

def draw_grid():
    pygame.draw.rect(screen, GRAY, (0, 100, WIDTH, HEIGHT - 100))
    for r in range(GRID_LEN):
        for c in range(GRID_LEN):
            value = grid[r][c]
            color = COLORS.get(value, BLACK)
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            if value:
                text = FONT.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def rotate_clockwise(mat):
    return [list(row) for row in zip(*mat[::-1])]

def move_left():
    global score
    moved = False
    new_grid = []
    for row in grid:
        tight = [i for i in row if i != 0]
        merged = []
        skip = False
        for i in range(len(tight)):
            if skip:
                skip = False
                continue
            if i + 1 < len(tight) and tight[i] == tight[i + 1]:
                merged.append(tight[i] * 2)
                score += tight[i] * 2
                skip = True
                moved = True
            else:
                merged.append(tight[i])
        merged += [0] * (GRID_LEN - len(merged))
        new_grid.append(merged)
        if merged != row:
            moved = True
    return new_grid, moved

def move(direction):
    global grid
    for _ in range(direction):
        grid = rotate_clockwise(grid)
    grid, moved = move_left()
    for _ in range((4 - direction) % 4):
        grid = rotate_clockwise(grid)
    if moved:
        new_tile()

def draw_header():
    global best_score
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 100))
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    best_text = FONT.render(f"Best: {best_score}", True, BLACK)
    restart_text = FONT.render("R - Restart", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (10, 50))
    screen.blit(restart_text, (250, 30))

def game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))
    screen.blit(overlay, (0, 0))
    text = BIG_FONT.render("Game Over!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def is_game_over():
    for r in range(GRID_LEN):
        for c in range(GRID_LEN):
            if grid[r][c] == 0:
                return False
            if c + 1 < GRID_LEN and grid[r][c] == grid[r][c + 1]:
                return False
            if r + 1 < GRID_LEN and grid[r][c] == grid[r + 1][c]:
                return False
    return True

reset_game()

running = True
while running:
    screen.fill(WHITE)
    draw_header()
    draw_grid()
    pygame.display.update()

    if is_game_over():
        game_over()
        if score > best_score:
            best_score = score
            with open("best_score.txt", "w") as f:
                f.write(str(best_score))
        reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > best_score:
                best_score = score
                with open("best_score.txt", "w") as f:
                    f.write(str(best_score))
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(LEFT)
            elif event.key == pygame.K_UP:
                move(UP)
            elif event.key == pygame.K_RIGHT:
                move(RIGHT)
            elif event.key == pygame.K_DOWN:
                move(DOWN)
            elif event.key == pygame.K_r:
                reset_game()

pygame.quit()
sys.exit()
