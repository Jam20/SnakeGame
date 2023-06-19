import pygame
from pygame.locals import *
from enum import Enum
from mimetypes import init
import random



#used to define a paticular point in the game's execution (synced to a frame)
class Node:
    def __init__(self, x, y, direction = None) -> None:
        self.x = x
        self.y = y
        self.direction = Direction.NONE

class Path:
    def __init__(self, width, height) -> None:
        self.grid = [[Node(x,y) for x in range(width)] for y in range(height)]
        print(width, height)
        if(height%2 == 0):
            for y, row in enumerate(self.grid):
                for x, node in enumerate(row):
                    if(x == 1 and y != 1): node.direction = Direction.UP
                    elif(y == height-1): node.direction = Direction.LEFT
                    elif(x== width-1 and y%2 == 1): node.direction = Direction.DOWN
                    elif(x== 2 and y%2 ==0): node.direction = Direction.DOWN
                    elif(y%2 == 0): node.direction = Direction.LEFT
                    else: node.direction = Direction.RIGHT
        else:
            print("Unable to make cycle")
    def __str__(self) -> str:
        output = ""
        for row in self.grid:
            for node in row:
                output += str(node.direction)
            output += '\n'

    def getDirectionFromGamestate(self, x,y):
        return self.grid[y][x].direction


#used to define a position on the board
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.x) + " " + str(self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

#used to define a object to be drawn to the screen
class Drawable:
    def __init__(self, drawFunc, position):
        self.drawFunc = drawFunc
        self.position = position

    
    def drawSelf(self, screen):
        self.drawFunc(screen, self.position)

#defines a direction for an object to travel in
class Direction(Enum):
    NONE  = 0
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    AI = 5

    def __str__(self) -> str:
        if(self == self.UP):
            return 'U'
        elif(self == self.DOWN):
            return 'D'
        elif(self == self.LEFT):
            return 'L'
        elif(self == self.RIGHT):
            return 'R'
        else:
            return 'N'

    @classmethod
    def getDirectionFromKey(cls, key):
        if key == pygame.K_w:
            return Direction.UP
        elif key == pygame.K_d:
            return Direction.RIGHT
        elif key == pygame.K_a:
            return Direction.LEFT
        elif key == pygame.K_s:
            return Direction.DOWN
        else:
            return Direction.NONE

    
    def isAngleValid(self, other):
        return 3 < self.value+other.value < 7
            
    def getNewPosition(self, pos):
        if(self == self.UP):
            return Pos(pos.x, pos.y-1)
        elif(self == self.DOWN):
            return Pos(pos.x, pos.y+1)
        elif(self == self.RIGHT):
            return Pos(pos.x+1, pos.y)
        elif(self == self.LEFT):
            return Pos(pos.x-1, pos.y)
        return pos



#used to define a snake in the game based on the positions of each of its blocks
class Snake(Drawable):
    def __init__(self, drawFunc, positions):
        self.drawFunc = drawFunc
        self.positions = positions
        self.isIncreasing = False

    def drawSelf(self, screen):
        for position in self.positions:
            self.drawFunc(screen, position)

    def getHeadPosition(self):
        return self.positions[0]

    def move(self, direction):
        posCopy = self.positions.copy()
        newPos = direction.getNewPosition(posCopy[0])
        posCopy.insert(0, newPos)
        if(not self.isIncreasing):
            posCopy.pop(-1)
        return Snake(self.drawFunc, posCopy)
    
    def increaseLength(self):
        self.isIncreasing = True

    def isCollidingWithSelf(self):
        for idx, pos in enumerate(self.positions):
            if idx != 0 and pos == self.getHeadPosition():
                return True
        return False

class Apple(Drawable):

    def eat(self, minX, minY, maxX, maxY, invalidPositions):
        isInvalidPos = True
        newPos = Pos(0,0)
        while isInvalidPos:
            isInvalidPos = False
            newPos = Pos(random.randint(minX,maxX),random.randint(minY,maxY))
            if(newPos.x == 0 or newPos.y == 0):
                isInvalidPos = True
                continue
            for pos in invalidPositions:
                if(newPos == pos):
                    isInvalidPos = True
                    break
            
        return Apple(self.drawFunc, newPos)

class GameState(Drawable):
    def __init__(self, snake, apple, score):
        self.snake = snake
        self.apple = apple
        self.score = score
    
    def moveApple(self, size):
        newApple = self.apple.eat(0,0,int(size[0]-1),int(size[1]-1), self.snake.positions)
        print(newApple.position)
        return GameState(self.snake, newApple, self.score)

    def update(self, direction, size, path):
        dir = direction
        if direction == Direction.AI:
            dir = path.getDirectionFromGamestate(self.snake.getHeadPosition().x, self.snake.getHeadPosition().y)
        newSnake = self.snake.move(dir)
        snakeHead = newSnake.getHeadPosition()
        if snakeHead.x < 1 or snakeHead.y < 1 or snakeHead.x >= size[0] or snakeHead.y >= size[1] or newSnake.isCollidingWithSelf():
            return GameState(Snake(newSnake.drawFunc, [Pos(5,5)]), Apple(self.apple.drawFunc, Pos(0,0)),0).moveApple(size)
        
        if newSnake.getHeadPosition() == self.apple.position:
            newSnake.increaseLength()
            newApple = self.moveApple(size).apple
            newScore = self.score + 1
            return GameState(newSnake, newApple, newScore)
        return GameState(newSnake, self.apple, self.score)
            
    def drawSelf(self, screen):
        self.snake.drawSelf(screen)
        self.apple.drawSelf(screen)

