import pygame
from pygame.locals import *

#Define Render Constants
size = (1000,1000)
blockSize = 10

borderColor = (255,0,0)
backgroundColor = (0,0,255)
snakeColor = (255,255,0)

#function which renders the text 
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

#wrapper for the text function in order to abstract to a simple message
def displayMessage(screen, text,x,y):
    textFont = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, textFont)
    TextRect.center = (x,y)
    screen.blit(TextSurf,TextRect)  

#Defining draw functions for different parts of the game
def drawBackground(screen, score, speed):
    screen.fill(borderColor)
    
    pygame.draw.rect(screen, backgroundColor, (0,0,size[0]-blockSize,size[1]-blockSize))
    displayMessage(screen, "Score: " + str(score),900,25)
    displayMessage(screen, "Speed: " + str(speed),100,25)

def drawSnakeBlock(screen, pos):
    screenPos = (pos.x*blockSize, pos.y * blockSize, blockSize, blockSize)
    pygame.draw.rect(screen, snakeColor, screenPos)

def drawApple(screen, pos):
    screenPos = (pos.x*blockSize, pos.y * blockSize, blockSize, blockSize)
    pygame.draw.rect(screen, borderColor, screenPos)
  
def renderFrame(screen, gameState, speed):
    drawBackground(screen, gameState.score, speed)
    gameState.drawSelf(screen)
    pygame.display.update()
