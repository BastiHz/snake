import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame as pg


TILE_SIZE = 40
WINDOW_WIDTH = 800  # should be multiple of tile size
WINDOW_HEIGHT = 600  # should be multiple of tile size
HEAD_COLOR = (255, 128, 0)
BODY_COLOR = (0, 155, 0)
FOOD_COLOR = (128, 0, 128)
BACKGROUND_COLORS = ((100, 15, 15), (15, 15, 15))
FPS = 60
SECONDS_PER_MOVE = 1/5
DIRECTIONS = {
    pg.K_w: (0, -1),
    pg.K_s: (0, 1),
    pg.K_a: (-1, 0),
    pg.K_d: (1, 0)
}


def make_new_food():
    while True:
        new_food = pg.Rect(
            random.choice(range(TILE_SIZE, WINDOW_WIDTH - TILE_SIZE, TILE_SIZE)),
            random.choice(range(TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE, TILE_SIZE)),
            TILE_SIZE,
            TILE_SIZE
        )
        if new_food.collidelist(snake) == -1:
            return new_food


pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "1"
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window_rect = window.get_rect()
head = pg.Rect(
    WINDOW_WIDTH // 2 // TILE_SIZE * TILE_SIZE,
    WINDOW_HEIGHT // 2 // TILE_SIZE * TILE_SIZE,
    TILE_SIZE,
    TILE_SIZE
)
snake = [head, head.move(-TILE_SIZE, 0), head.move(-TILE_SIZE * 2, 0)]
time_since_last_move = 0
direction = (1, 0)
old_direction = direction
food = make_new_food()
running = True
snake_alive = True
game_started = False
grow = False
clock = pg.time.Clock()
while running:
    dt = clock.tick(FPS) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key in DIRECTIONS:
                new_direction = DIRECTIONS[event.key]
                # prevent the snake from reversing into itself
                if new_direction[0] != old_direction[0] * -1 or \
                        new_direction[0] != old_direction[0] * -1:
                    direction = new_direction
            if not game_started:
                # press any key to start
                game_started = True

    if snake_alive and game_started:
        if snake[0].colliderect(food):
            grow = True
            food = make_new_food()
        time_since_last_move += dt
        if time_since_last_move >= SECONDS_PER_MOVE:
            time_since_last_move -= SECONDS_PER_MOVE
            old_direction = direction
            new_head = snake[0].move(
                direction[0] * TILE_SIZE,
                direction[1] * TILE_SIZE
            )
            snake.insert(0, new_head)
            if grow:
                grow = False
                # grow by not removing the end
            else:
                snake.pop()

    window.fill(BACKGROUND_COLORS[snake_alive])
    for rect in snake[1:]:
        pg.draw.rect(window, BODY_COLOR, rect)
    pg.draw.rect(window, HEAD_COLOR, snake[0])
    pg.draw.circle(window, FOOD_COLOR, food.center, food.width // 2)

    snake_alive = snake[0].colliderect(window_rect) and \
        snake[0].collidelist(snake[1:]) == -1

    pg.display.flip()
