import threading
import time
import pygame
from pygame.locals import *
from render import *
from gamestate import Apple, Direction, GameState, Snake, Pos, Path

#used to actually run the game

#define gameloop variables
speed = 1
baseSpeed = 15
running = True
direction = Direction.NONE
gameSize = (size[0]//10-1, size[1]//10-1)
gameState = GameState(Snake(drawSnakeBlock, [Pos(5,5)]), Apple(drawApple, Pos(0,0)),0).moveApple(gameSize)
#start game
pygame.init()
screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Snake")
path = Path(gameSize[0], gameSize[1])
print(path.grid[gameSize[1]-1][0].direction)
#start gameState updator
def gameStateThread():
    global gameState
    while running:
        gameState = gameState.update(direction, gameSize, path)
        time.sleep(1/(speed*15))

gameThread = threading.Thread(target= gameStateThread)
gameThread.start()

isHumanControl = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            set_screen_size(event.dict['size'])
            size = event.dict['size']
            gameSize = (size[0]//10-1, size[1]//10-1)
            path = Path(gameSize[0], gameSize[1])
            gameState = gameState.moveApple(gameSize)
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
                newDirection = Direction.getDirectionFromKey(event.key)
                if direction == Direction.NONE or newDirection.isAngleValid(direction):
                    direction = newDirection
            elif event.key == pygame.K_r:
                isHumanControl = True
    if not isHumanControl:
        direction = Direction.AI
    gameSize = (size[0]//10-1, size[1]//10-1)
    renderFrame(screen, gameState, speed)



            
