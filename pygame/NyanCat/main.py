import pygame

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Nyan Cat')

# Цвета
DARK_BLUE = (10, 10, 40)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)


# КЛАССЫ
class Cat:
    """Класс игрового персонажа - кота"""
    def __init__(self):
        self.width = 100
        self.height = 64
        self.x = 0
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 7
        self.color = PINK
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """Отрисовка кота"""
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, keys):
        """Обновление позиции кота"""
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y += self.speed

        self.rect.topleft = (self.x, self.y)


# Инициализация игры
clock = pygame.time.Clock()
running = True
cat = Cat()

# Главный игровой цикл
while running:
    current_time = pygame.time.get_ticks()
    dt = clock.tick(60) / 1000

    WIN.fill(DARK_BLUE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление состояния
    keys = pygame.key.get_pressed()

    # Обновление кота
    cat.update(keys)
    cat.draw(WIN)
    pygame.display.update()     # Обновление экрана

pygame.quit()