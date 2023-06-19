import threading
import time
import pygame
from pygame.locals import RESIZABLE, VIDEORESIZE
from render import draw_snake_block, draw_apple, set_screen_size, render_frame
from render import size
from gamestate import Apple, Direction, GameState, Snake, Pos, Path

# used to actually run the game

# define gameloop variables
speed = 1
baseSpeed = 15
running = True
direction = Direction.NONE
gameSize = (size[0] // 10 - 1, size[1] // 10 - 1)
gameState = GameState(
    Snake(draw_snake_block, [Pos(5, 5)]), Apple(draw_apple, Pos(0, 0)), 0
).move_apple(gameSize)
# start game
pygame.init()
screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Snake")
path = Path(gameSize[0], gameSize[1])
print(path.grid[gameSize[1] - 1][0].direction)


# start gameState updator
def gameStateThread():
    global gameState
    while running:
        gameState = gameState.update(direction, gameSize, path)
        time.sleep(1 / (speed * 15))


gameThread = threading.Thread(target=gameStateThread)
gameThread.start()

isHumanControl = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict["size"], RESIZABLE)
            set_screen_size(event.dict["size"])
            size = event.dict["size"]
            gameSize = (size[0] // 10 - 1, size[1] // 10 - 1)
            path = Path(gameSize[0], gameSize[1])
            gameState = gameState.move_apple(gameSize)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and speed > 1:
                speed -= 1
                continue
            elif event.key == pygame.K_e:
                speed += 1
                continue
            if isHumanControl:
                if event.key == pygame.K_r:
                    isHumanControl = False
                newDirection = Direction.get_direction_for_key(event.key)
                direction = newDirection if newDirection.is_angle_valid(direction) else direction
            elif event.key == pygame.K_r:
                isHumanControl = True
    if not isHumanControl:
        direction = Direction.AI
    gameSize = (size[0] // 10 - 1, size[1] // 10 - 1)
    render_frame(screen, gameState, speed)
