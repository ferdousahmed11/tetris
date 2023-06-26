import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
# Define the dimensions of the game grid
grid_size = 30
grid_width = window_width // grid_size
grid_height = window_height // grid_size

# Define the shapes of the tetrominoes
tetromino_shapes = [
    [[1, 1, 1, 1]],                             # I-shape
    [[1, 1], [1, 1]],                           # O-shape
    [[1, 1, 1], [0, 1, 0]],                     # T-shape
    [[1, 1, 0], [0, 1, 1]],                     # Z-shape
    [[0, 1, 1], [1, 1, 0]],                     # S-shape
    [[1, 1, 1], [1, 0, 0]],                     # L-shape
    [[1, 1, 1], [0, 0, 1]],                     # J-shape
]

# Define the colors of the tetrominoes
tetromino_colors = [
    CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE
]

# Define the initial position of the falling tetromino
initial_x = grid_width // 2
initial_y = 0

# Initialize the game grid
grid = [[BLACK] * grid_width for _ in range(grid_height)]


def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(window, grid[y][x], (x * grid_size, y * grid_size, grid_size, grid_size), 0)


def draw_tetromino(tetromino, x, y, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                pygame.draw.rect(window, color, (
                    (x + col) * grid_size, (y + row) * grid_size, grid_size, grid_size), 0)


def check_collision(tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                if x + col < 0 or x + col >= grid_width or y + row >= grid_height or grid[y + row][x + col] != BLACK:
                    return True
    return False


def place_tetromino(tetromino, x, y, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                grid[y + row][x + col] = color


def remove_completed_rows():
    full_rows = []
    for row in range(grid_height):
        if all(cell != BLACK for cell in grid[row]):
            full_rows.append(row)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * grid_width)


def game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(window_width / 2, window_height / 2))
    window.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def run_game():
    clock = pygame.time.Clock()
    tetromino = random.choice(tetromino_shapes)
    tetromino_color = random.choice(tetromino_colors)
    x, y = initial_x, initial_y
    game_over_flag = False

    while not game_over_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_flag = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(tetromino, x - 1, y):
                        x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(tetromino, x + 1, y):
                        x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(tetromino, x, y + 1):
                        y += 1
                elif event.key == pygame.K_SPACE:
                    rotated_tetromino = list(zip(*reversed(tetromino)))
                    if not check_collision(rotated_tetromino, x, y):
                        tetromino = rotated_tetromino

        if not check_collision(tetromino, x, y + 1):
            y += 1
        else:
            place_tetromino(tetromino, x, y, tetromino_color)
            remove_completed_rows()
            tetromino = random.choice(tetromino_shapes)
            tetromino_color = random.choice(tetromino_colors)
            x, y = initial_x, initial_y
            if check_collision(tetromino, x, y):
                game_over_flag = True

        window.fill(BLACK)
        draw_grid()
        draw_tetromino(tetromino, x, y, tetromino_color)
        pygame.display.flip()
        clock.tick(5)

    game_over()
    pygame.quit()


if __name__ == "__main__":
    run_game()
