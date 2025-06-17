import pygame
import random
import time
import sys

# Game size
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Maze AI")
clock = pygame.time.Clock()

# colours used in th game
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 40)

# Settings of the game
CELL_SIZE = 40
preview_time = 3  # seconds
max_levels = 10
TIMER_LIMIT = 30  # seconds per level


def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []
    visited = [[False]*cols for _ in range(rows)]

    def carve(x, y):
        directions = [(0,-1),(1,0),(0,1),(-1,0)]
        random.shuffle(directions)
        visited[y][x] = True
        maze[y][x] = 0
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                maze[y+dy][x+dx] = 0
                carve(nx, ny)

    carve(0, 0)
    return maze

def draw_maze(maze, player, goal, hidden=False):
    screen.fill(WHITE)
    rows, cols = len(maze), len(maze[0])
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif hidden:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.draw.rect(screen, GREEN, (goal[0]*CELL_SIZE, goal[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (player[0]*CELL_SIZE, player[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_message(text):
    screen.fill(WHITE)
    label = font.render(text, True, RED)
    screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
    pygame.display.update()

def draw_timer(time_left):
    timer_text = font.render(f"Time Left: {time_left}s", True, RED)
    screen.blit(timer_text, (10, 10))

def level_complete_animation(level):
    duration = 2  # seconds
    start_time = time.time()
    alpha = 0
    text_surface = font.render(f"Level {level} Complete!", True, (0, 0, 0))
    while time.time() - start_time < duration:
        screen.fill(WHITE)
        alpha = abs(int((time.time() - start_time) * 255 / duration * 2) % 255)
        animated_text = text_surface.copy()
        animated_text.set_alpha(alpha)
        screen.blit(animated_text, (WIDTH//2 - animated_text.get_width()//2, HEIGHT//2 - animated_text.get_height()//2))
        pygame.display.update()
        clock.tick(60)

def game_over_animation():
    screen.fill(WHITE)
    text = font.render("⛔ Time's Up! Game Over.", True, RED)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def main():
    level = 1

    while level <= max_levels:
        rows = cols = min(15, 5 + level*2)
        maze = generate_maze(rows, cols)
        player = [0, 0]
        goal = [cols-1, rows-1]

        # Preview phase
        draw_maze(maze, player, goal, hidden=False)
        pygame.display.update()
        time.sleep(preview_time)

        # Timer to complete the game
        start_time = time.time()

        # Game loop continues 
        playing = True
        while playing:
            elapsed = int(time.time() - start_time)
            time_left = max(0, TIMER_LIMIT - elapsed)

            if time_left == 0:
                game_over_animation()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_UP]: dy = -1
            if keys[pygame.K_DOWN]: dy = 1
            if keys[pygame.K_LEFT]: dx = -1
            if keys[pygame.K_RIGHT]: dx = 1
            new_x = player[0] + dx
            new_y = player[1] + dy

            if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] == 0:
                player = [new_x, new_y]
                time.sleep(0.1)
            draw_maze(maze, player, goal, hidden=True)
            draw_timer(time_left)
            pygame.display.update()
            clock.tick(30)
            if player == goal:
                level_complete_animation(level)
                level += 1
                break

    show_message("🏆 You finally Beat the Game!")
    pygame.time.delay(3000)
    pygame.quit()
if __name__ == "__main__":
    main()
