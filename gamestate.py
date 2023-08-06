from typing import Callable
from pygame import Surface
import pygame
from enum import Enum
from random import randint


# used to define a position on the board
class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({str(self.x)}, {str(self.y)})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


# used to define a paticular point in the game's execution (synced to a frame)
class Direction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    AI = 5

    def __str__(self) -> str:
        match self:
            case self.UP:
                return "U"
            case self.DOWN:
                return "D"
            case self.LEFT:
                return "L"
            case self.RIGHT:
                return "R"
            case _:
                return "N"

    @classmethod
    def get_direction_for_key(cls, key: int):
        match key:
            case pygame.K_w:
                return Direction.UP
            case pygame.K_d:
                return Direction.RIGHT
            case pygame.K_a:
                return Direction.LEFT
            case pygame.K_s:
                return Direction.DOWN
            case _:
                return Direction.NONE

    def is_angle_valid(self, other: Enum) -> bool:
        if self == Direction.NONE:
            return True
        return 3 < self.value + other.value < 7

    def get_new_position(self, pos: Pos) -> Pos:
        match self:
            case self.UP:
                return Pos(pos.x, pos.y - 1)
            case self.DOWN:
                return Pos(pos.x, pos.y + 1)
            case self.LEFT:
                return Pos(pos.x - 1, pos.y)
            case self.RIGHT:
                return Pos(pos.x + 1, pos.y)
            case _:
                return pos


class Node(Pos):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.direction = Direction.NONE


class Path:
    def __init__(self, width: int, height: int) -> None:
        self.grid = [[Node(x, y) for x in range(width)] for y in range(height)]
        if height % 2 == 1:
            for y, row in enumerate(self.grid):
                for x, node in enumerate(row):
                    if x == 1 and y != 1:
                        node.direction = Direction.UP
                    elif y == height - 1:
                        node.direction = Direction.LEFT
                    elif x == width - 1 and y % 2 == 1:
                        node.direction = Direction.DOWN
                    elif x == 2 and y % 2 == 0:
                        node.direction = Direction.DOWN
                    elif y % 2 == 0:
                        node.direction = Direction.LEFT
                    else:
                        node.direction = Direction.RIGHT
        else:
            print("Unable to make cycle")

    def __str__(self) -> str:
        output = ""
        for row in self.grid:
            for node in row:
                output += str(node.direction)
            output += "\n"
        return output

    def get_direction_for_node(self, pos: Pos) -> Direction:
        return self.grid[pos.y][pos.x].direction


# used to define a object to be drawn to the screen
class Drawable:
    def __init__(self, draw_func: Callable[[Surface, Pos], None], pos: Pos):
        self.draw_func = draw_func
        self.position = pos

    def draw_self(self, screen: Surface) -> None:
        self.draw_func(screen, self.position)


# defines a direction for an object to travel in


# used to define a snake in the game based on the positions of all its blocks
class Snake(Drawable):
    def __init__(self, drawFunc: Callable[[Surface, Pos], None], posList: list[Pos]):
        super().__init__(drawFunc, posList[0])
        self.positions = posList
        self.isIncreasing = False

    def draw_self(self, screen: Surface) -> None:
        for position in self.positions:
            self.draw_func(screen, position)

    def get_head_position(self) -> Pos:
        return self.positions[0]

    def get_length(self) -> int:
        return len(self.positions)

    def move(self, direction: Direction):
        posCopy = self.positions.copy()
        newPos = direction.get_new_position(posCopy[0])
        posCopy.insert(0, newPos)
        if not self.isIncreasing:
            posCopy.pop(-1)
        return Snake(self.draw_func, posCopy)

    def increase_length(self) -> None:
        self.isIncreasing = True

    def is_colliding_with_self(self) -> bool:
        for idx, pos in enumerate(self.positions):
            if idx != 0 and pos == self.get_head_position():
                return True
        return False


class Apple(Drawable):
    def eat(self, min: Pos, max: Pos, invalid: list[Pos]):
        isInvalidPos = True
        newPos = Pos(0, 0)
        while isInvalidPos:
            isInvalidPos = False
            newPos = Pos(randint(min.x, max.x), randint(min.y, max.y))
            if newPos.x == 0 or newPos.y == 0:
                isInvalidPos = True
                continue
            for pos in invalid:
                if newPos == pos:
                    isInvalidPos = True
                    break

        return Apple(self.draw_func, newPos)


class GameState(Drawable):
    def __init__(self, snake: Snake, apple: Apple, score: int):
        self.snake = snake
        self.apple = apple
        self.score = score

    def move_apple(self, size: tuple[int, int]):
        minPos = Pos(0, 0)
        maxPos = Pos(int(size[0] - 1), int(size[1] - 1))
        newApple = self.apple.eat(minPos, maxPos, self.snake.positions)
        return GameState(self.snake, newApple, self.score)

    def update(self, dir: Direction, size: tuple[int, int], path: Path):
        # type: (Direction, tuple[int, int], Path) -> GameState
        dir = dir
        if dir == Direction.AI:
            dir = get_best_move(self, size[0], size[1])
            # dir = path.get_direction_for_node(self.snake.get_head_position())

        newSnake = self.snake.move(dir)
        snakeHead = newSnake.get_head_position()
        if (
            snakeHead.x < 1
            or snakeHead.y < 1
            or snakeHead.x >= size[0]
            or snakeHead.y >= size[1]
            or newSnake.is_colliding_with_self()
        ):
            print(
                f"died in state: {last_state} apple: {self.apple.position} head: {self.snake.position} direction: {dir}"
            )
            return GameState(
                Snake(newSnake.draw_func, [Pos(5, 5)]),
                Apple(self.apple.draw_func, Pos(0, 0)),
                0,
            ).move_apple(size)

        if newSnake.get_head_position() == self.apple.position:
            newSnake.increase_length()
            newApple = self.move_apple(size).apple
            newScore = self.score + 1
            return GameState(newSnake, newApple, newScore)
        return GameState(newSnake, self.apple, self.score)

    def draw_self(self, screen):
        self.snake.draw_self(screen)
        self.apple.draw_self(screen)


class State(Enum):
    DEFAULT = 0
    DOWNSEEK = 1
    UPSEEK = 2


upseek_rows = set()
downseek_rows = set()
last_state = State.DEFAULT


def get_best_move(game_state: GameState, width: int, height: int):
    global last_state
    snake_pos = game_state.snake.get_head_position()
    snake_tail_pos = game_state.snake.positions[-1]
    apple_pos = game_state.apple.position
    state = get_new_state(
        snake_pos,
        snake_tail_pos,
        game_state.snake.get_length(),
        apple_pos,
        last_state,
        width,
    )
    move = Direction.NONE
    match state:
        case State.DEFAULT:
            move = get_default_move(snake_pos, width, height)
        case State.DOWNSEEK:
            move = get_downseek_move(snake_pos, apple_pos, width, height)
        case State.UPSEEK:
            move = get_upseek_move(snake_pos, apple_pos, width, height)
    last_state = state
    return move


def get_new_state(
    snake_pos: Pos,
    snake_tail_pos: Pos,
    snake_length: int,
    apple_pos: Pos,
    last_state: State,
    width: int,
) -> State:
    global downseek_rows
    match last_state:
        case State.DEFAULT:
            if snake_pos.y > snake_tail_pos.y and snake_tail_pos.x > 1 or snake_pos.y in upseek_rows:
                # print("Transition to Down seek")
                return State.DOWNSEEK
            else:
                return State.DEFAULT
        case State.DOWNSEEK:
            if snake_pos.x == 1:
                # print("Transition to UpSeek")
                upseek_rows.clear()
                return State.UPSEEK
            else:
                downseek_rows.add(apple_pos.y)
                return State.DOWNSEEK
        case State.UPSEEK:
            if (
                snake_pos.y == 1
                or (apple_pos.y < snake_tail_pos.y and snake_pos.x == 1)
                or (
                    apple_pos.y in downseek_rows
                    or apple_pos.y + 1 in downseek_rows
                    or apple_pos.y - 1 in downseek_rows
                )
                or apple_pos.y * width < snake_length
            ):
                # print("Transition to Default")
                downseek_rows.clear()
                return State.DEFAULT
            else:
                upseek_rows.add(apple_pos.y)
                return State.UPSEEK
    return State.DEFAULT


def get_downseek_move(
    snake_pos: Pos, apple_pos: Pos, width: int, height: int
) -> Direction:
    x, y = snake_pos.x, snake_pos.y
    if y == 1:
        if x == width - 1:
            return Direction.DOWN
        else:
            return Direction.RIGHT
    elif y == height - 1:
        if x == 1:
            return Direction.UP
        else:
            return Direction.LEFT
    elif y % 2 == 0:
        if x == 1:
            return Direction.UP
        elif x == 2:
            if apple_pos.y < y:
                return Direction.LEFT
            else:
                return Direction.DOWN
        elif x == width - 1:
            if apple_pos.y - 1 > y:
                return Direction.DOWN
            else:
                return Direction.LEFT
        else:
            return Direction.LEFT
    else:
        if x == 1:
            return Direction.UP
        elif x == 2:
            if apple_pos.y < y:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        elif x == width - 1:
            return Direction.DOWN
        else:
            return Direction.RIGHT


def get_upseek_move(snake_pos: Pos, apple_pos: Pos, width: int, height: int):
    x, y = snake_pos.x, snake_pos.y
    if y == 1:
        if x == width - 1:
            return Direction.DOWN
        else:
            return Direction.RIGHT
    elif y == height - 1:
        if x == 1:
            return Direction.UP
        else:
            return Direction.LEFT
    elif y % 2 == 0:
        if x == 1:
            return Direction.UP
        else:
            return Direction.LEFT
    else:
        if x == 1:
            if abs(y - apple_pos.y) <= 1 and apple_pos.x > 1:
                return Direction.RIGHT
            else:
                return Direction.UP
        elif x == width - 2:
            return Direction.UP
        else:
            return Direction.RIGHT


def get_default_move(pos: Pos, width: int, height: int) -> Direction:
    x, y = pos.x, pos.y
    if y == 1:
        if x == width - 1:
            return Direction.DOWN
        else:
            return Direction.RIGHT
    elif y == height - 1:
        if x == 1:
            return Direction.UP
        else:
            return Direction.LEFT
    elif y % 2 == 0:
        if x == 1:
            return Direction.UP
        elif x == 2:
            return Direction.DOWN
        else:
            return Direction.LEFT
    else:
        if x == 1:
            return Direction.UP
        elif x == width - 1:
            return Direction.DOWN
        else:
            return Direction.RIGHT
