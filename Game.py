import pygame
from pygame.locals import *
import random
import threading
import time


#Game Startup
pygame.init()
screen = pygame.display.set_mode((1000,1000), RESIZABLE)
pygame.display.set_caption("Snake")
running = True
direction = 3
score = 0
timespeed = 1
size = (1000,1000)
aiControl = False


#Class which defines each section of the snake each with its own position
#Singly Linked to the head of the snake and are drawn recursivly 
class snakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

    def drawSelf(self):
        pygame.draw.rect(screen, (255,255,0), (self.x*10, self.y*10, 10, 10))
        if(self.next != None):
            self.next.drawSelf()

#Class which defines the apple which the snake needs
#contains a position and a function to draw itself
class appleObj:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def drawApple(self):
        pygame.draw.rect(screen, (255,0,0), (self.x*10, self.y*10, 10, 10))

#Function used to draw the snake at the begining of the game
def createSnake():
    head = snakeBlock(random.randint(10,90), random.randint(10,90))
    head.next = snakeBlock(head.x+1,head.y)
    head.next.next = snakeBlock(head.x+2,head.y)
    head.next.next.next = snakeBlock(head.x+3,head.y)
    head.next.next.next.next = snakeBlock(head.x+4,head.y)
    return head

#Function used to recursivly move the other segments of the snake
def followPrev(prev):
    if(prev.next.next != None):
        followPrev(prev.next)
    prev.next.x = prev.x
    prev.next.y = prev.y

#function used to move the head of the snake
#calls followPrev() in order to move the rest of the snake
def moveDirection(snake, dir):
    followPrev(snake)
    if dir == 0:
        snake.y-=1
    elif dir == 1:
        snake.x +=1
    elif dir == 2:
        snake.y+=1
    elif dir == 3:
        snake.x-=1

#Function which adds a new segment to the snake when the apple is collected
def addToSnake(snake):
    currentNode = snake
    while currentNode.next.next != None:
        currentNode = currentNode.next
    currentNode.next.next = snakeBlock(currentNode.next.x-currentNode.x,currentNode.next.y-currentNode.y)

#Function which creates a new apple when one is collected
def createNewApple(snake):
    newappX = random.randint(1,99)
    newappY = random.randint(1,99)
    goodLocation = False
    currentNode = snake
    while goodLocation == False:
        while currentNode!= None:
            if(newappX == currentNode.x and newappY == currentNode.y):
                goodLocation = False
            else:
                goodLocation = True
            currentNode = currentNode.next
        currentNode = snake
        newappX = random.randint(1,99)
        newappY = random.randint(1,99)
    return appleObj(newappX,newappY)

#Function which checks to see if the snake has collided with the apple
def checkAppleCollision(snake, apple):
    if(snake.x == apple.x and snake.y == apple.y):
        addToSnake(snake)
        return True
    return False

#function which renders the text 
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

#wrapper for the text function in order to abstract to a simple message
def displayMessage(text,x,y):
    textFont = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, textFont)
    TextRect.center = (x,y)
    screen.blit(TextSurf,TextRect)

#function which checks if the snake has collided with itself
def checkSnakecollision(snake,dir,size):
    if(snake.x>size[0]/10 or snake.x<1 or snake.y<1 or snake.y>size[1]/10):
        return True
    else:
        currentNode = snake.next
        while currentNode != None:
            if(snake.x == currentNode.x and snake.y == currentNode.y):
                return True
            currentNode = currentNode.next
        return False




#function used to run the thread controlling the movement of the snake
def movementManager():
    while running:
        time.sleep(1/(timespeed*10))
        moveDirection(snakeHead,direction)

#starts up movment thread and final setup
snakeHead = createSnake()
appleHead = createNewApple(snakeHead)
movementThread = threading.Thread(target=movementManager)
movementThread.start()
#Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            size = event.dict['size']
            appleHead = createNewApple(snakeHead)
            pygame.display.update()
        elif event.type == pygame.KEYDOWN:
            if not aiControl:
                if event.key==pygame.K_w and  direction !=2:
                    direction = 0
                elif event.key==pygame.K_d and direction !=3:
                    direction = 1
                elif event.key==pygame.K_s and direction !=0:
                    direction = 2
                elif event.key==pygame.K_a and direction !=1:
                    direction = 3
            else:
                direction = 0
                #direction = getNextMove(snakeHead,appleHead,direction,score)
            if event.key==pygame.K_q:
                if timespeed>1:
                    timespeed = timespeed-1
            elif event.key==pygame.K_e:
                timespeed=timespeed+1
            if event.key==pygame.K_x:
                aiControl = not aiControl
    screen.fill((0,0,255))
    pygame.draw.rect(screen, (255,0,0), (0,0,size[0],10))
    pygame.draw.rect(screen, (255,0,0), (0,0,10,size[1]))
    pygame.draw.rect(screen, (255,0,0), (0,size[1]-10,size[0],10))
    pygame.draw.rect(screen, (255,0,0), (size[0]-10,0,10,size[1]))
    displayMessage("Score: " + str(score),900,25)
    displayMessage("Speed: " + str(timespeed),100,25)
    snakeHead.drawSelf()
    appleHead.drawApple()
    pygame.display.update()
    if checkAppleCollision(snakeHead,appleHead):
        appleHead = createNewApple(snakeHead)
        score +=1
    if checkSnakecollision(snakeHead,direction,size):
        snakeHead = createSnake()
        direction = 3
        appleHead = createNewApple(snakeHead)
        score = 0
    
    #moveDirection(snakeHead,direction)
    
    
    
pygame.quit()

    
    