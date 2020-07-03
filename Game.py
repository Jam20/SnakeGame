import pygame
import random
pygame.init()
screen = pygame.display.set_mode([1000,1000])

class snakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

    def drawSelf(self):
        pygame.draw.rect(screen, (255,255,0), (self.x*10, self.y*10, 10, 10))
        if(self.next != None):
            self.next.drawSelf()

class appleObj:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def drawApple(self):
        pygame.draw.rect(screen, (255,0,0), (self.x*10, self.y*10, 10, 10))


def createSnake():
    head = snakeBlock(random.randint(10,90), random.randint(10,90))
    head.next = snakeBlock(head.x+1,head.y)
    head.next.next = snakeBlock(head.x+2,head.y)
    head.next.next.next = snakeBlock(head.x+3,head.y)
    head.next.next.next.next = snakeBlock(head.x+4,head.y)

    return head
def followPrev(prev):
    if(prev.next.next != None):
        followPrev(prev.next)
    prev.next.x = prev.x
    prev.next.y = prev.y
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
def addToSnake(snake):
    currentNode = snake
    while currentNode.next.next != None:
        currentNode = currentNode.next
    currentNode.next.next = snakeBlock(currentNode.next.x-currentNode.x,currentNode.next.y-currentNode.y)
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

def checkAppleCollision(snake, apple):
    if(snake.x == apple.x and snake.y == apple.y):
        addToSnake(snake)
        return True
    return False

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def displayMessage(text):
    textFont = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, textFont)
    TextRect.center = (900,25)
    screen.blit(TextSurf,TextRect)

def checkSnakecollision(snake,dir):
    if(snake.x>98 or snake.x<1 or snake.y<1 or snake.y>98):
        return True
    else:
        currentNode = snake.next
        while currentNode != None:
            if(snake.x == currentNode.x and snake.y == currentNode.y):
                return True
            currentNode = currentNode.next
        return False


pygame.display.set_caption("Snake")

running = True
direction = 3
snakeHead = createSnake()
appleHead = createNewApple(snakeHead)
score = 0


while running:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,255))
    pygame.draw.rect(screen, (255,0,0), (0,0,1000,10))
    pygame.draw.rect(screen, (255,0,0), (0,0,10,1000))
    pygame.draw.rect(screen, (255,0,0), (0,990,1000,10))
    pygame.draw.rect(screen, (255,0,0), (990,0,10,1000))
    displayMessage("Score: " + str(score))
    snakeHead.drawSelf()
    appleHead.drawApple()
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] and  direction !=2):
        direction = 0
    elif keys[pygame.K_d] and direction !=3:
        direction = 1
    elif keys[pygame.K_s] and direction !=0:
        direction = 2
    elif keys[pygame.K_a] and direction !=1:
        direction = 3
    if checkAppleCollision(snakeHead,appleHead):
        appleHead = createNewApple(snakeHead)
        score +=1
    if checkSnakecollision(snakeHead,direction):
        snakeHead = createSnake()
        direction = 3
        appleHead = createNewApple(snakeHead)
        score = 0
    moveDirection(snakeHead,direction)
    
    
    

pygame.quit()

    
    