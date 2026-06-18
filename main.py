"""Игра «Змейка» на pygame."""

from random import randint

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
CELL_SIZE = GRID_SIZE
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK
GREEN = (0, 255, 0)
RED = (255, 0, 0)

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=CENTER, body_color=None):
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на игровом поле."""


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions):
        """Инициализирует яблоко."""
        super().__init__(body_color=RED)
        self.occupied_positions = occupied_positions
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        while True:
            x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x_position, y_position)
            if self.position not in self.occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = (*self.position, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(body_color=GREEN)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.position = CENTER
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions:
            rect = (*position, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)

    def move(self):
        """Перемещает змейку в текущем направлении."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        x_position, y_position = self.get_head_position()
        dx_position, dy_position = self.direction

        new_head = (
            (x_position + dx_position * GRID_SIZE) % SCREEN_WIDTH,
            (y_position + dy_position * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        opposite_directions = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT,
        }

        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Запускает основной игровой цикл."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(20)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
