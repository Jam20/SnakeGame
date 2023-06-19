from pygame import Surface, Rect, draw, font, display
from gamestate import GameState, Pos

# Define Render Constants
size = (1000, 790)
blockSize = 10

borderColor = (255, 0, 0)
backgroundColor = (0, 0, 255)
snakeColor = (255, 255, 0)


def set_screen_size(newSize: tuple[int, int]):
    global size
    size = newSize


# function which renders the text
def text_objects(text: str, font: font.Font) -> tuple[Surface, Rect]:
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


# wrapper for the text function in order to abstract to a simple message
def display_message(screen: Surface, text: str, x: int, y: int) -> None:
    textFont = font.Font("freesansbold.ttf", 30)
    TextSurf, TextRect = text_objects(text, textFont)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)


# Defining draw functions for different parts of the game
def draw_background(screen: Surface, score: int, speed: int) -> None:
    screen.fill(borderColor)

    def border(size: int) -> int:
        return size - 2 * blockSize

    draw.rect(
        screen,
        backgroundColor,
        (blockSize, blockSize, border(size[0]), border(size[0])),
    )
    display_message(screen, "Score: " + str(score), 900, 25)
    display_message(screen, "Speed: " + str(speed), 100, 25)


def draw_snake_block(screen: Surface, pos: Pos):
    drawBlock(screen, pos, snakeColor)


def draw_apple(screen: Surface, pos: Pos):
    drawBlock(screen, pos, borderColor)


def drawBlock(screen: Surface, pos: Pos, color: tuple[int, int, int]):
    screenPos = (pos.x * blockSize, pos.y * blockSize, blockSize, blockSize)
    draw.rect(screen, color, screenPos)


def render_frame(screen: Surface, gameState: GameState, speed: int):
    draw_background(screen, gameState.score, speed)
    gameState.draw_self(screen)
    display.update()
