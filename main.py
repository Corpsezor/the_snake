import pygame
from random import randint

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE   
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

class GameObject:
    def __init__(self, position=CENTER, body_color=None):
        """Базовый класс для всех игровых объектов."""

        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        pass

class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__(body_color=RED)  
        self.randomize_position()
    
    def randomize_position(self):  
        """Устанавливает случайную позицию яблока."""
        self.position = (randint(0, SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE * CELL_SIZE,
                         randint(0, SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE * CELL_SIZE)
        
    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        pygame.draw.rect(screen, self.body_color, (*self.position, CELL_SIZE, CELL_SIZE))

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
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for pos in self.positions:
            pygame.draw.rect(screen, self.body_color, (*pos, CELL_SIZE, CELL_SIZE))
        if len(self.positions) > 1:
            tail = self.positions[-1]
            pygame.draw.rect(screen, BLACK, (*tail, CELL_SIZE, CELL_SIZE))  

    def move(self):
        """Перемещает змейку в текущем направлении."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((x + dx * CELL_SIZE) % SCREEN_WIDTH, 
                    (y + dy * CELL_SIZE) % SCREEN_HEIGHT)
        if  new_head in self.positions:  
            self.reset()
        else: 
            self.positions.insert(0, new_head)  
            if len(self.positions) > self.length:
                self.positions.pop()  

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        opposite_directions = {(0, -1): (0, 1), (0, 1): (0, -1), 
                               (-1, 0): (1, 0), (1, 0): (-1, 0)}
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction

def main():
    """Основной игровой цикл."""
    clock = pygame.time.Clock()
    
    snake = Snake()
    apple = Apple()
    
    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)
        
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        
        screen.fill(BLACK)
        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()


