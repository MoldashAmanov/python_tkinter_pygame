import pygame
import random
import os

# Инициализация
pygame.init()

# Модуль шрифтов
pygame.font.init()

# Константы
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Nyan Cat')

# Шрифт
FONT = 'Arial'

# Цвета
DARK_BLUE = (10, 10, 40)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)


# Загружаем изображения
nyan_frames = []
for i in range(6):
    try:
        frame = pygame.image.load(f'images/cat/{i}.png')
        frame = pygame.transform.scale(frame, (frame.get_width() // 6, frame.get_height() // 6))
        nyan_frames.append(frame)
    except:
        print(f'Не удалось загрузить кадр {i}.png')

if not nyan_frames:
    dummy_frame = pygame.Surface((100, 64))
    dummy_frame.fill('PINK')
    nyan_frames = [dummy_frame] * 5

# Загрузка изображений еды
GOOD_IMAGES = []
BAD_IMAGES = []

try:
    for filename in os.listdir('images/good'):
        img = pygame.image.load(os.path.join('images/good', filename)).convert_alpha()
        img = pygame.transform.scale(img, (48, 48))
        GOOD_IMAGES.append(img)

    for filename in os.listdir('images/bad'):
        img = pygame.image.load(os.path.join('images/bad', filename)).convert_alpha()
        img = pygame.transform.scale(img, (48, 48))
        BAD_IMAGES.append(img)
except:
    print('Не удалось загрузить изображение еды')


# КЛАССЫ
class Cat:
    """Класс игрового персонажа - кота"""
    def __init__(self):
        self.width = 100
        self.height = 64
        self.x = 0
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 7
        self.animation_speed = 0.2
        self.frames = nyan_frames
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return self.image

    def draw(self, surface):
        """Отрисовка кота"""
        surface.blit(self.animate(), (self.rect.x, self.rect.y))

    def update(self, keys):
        """Обновление позиции кота"""
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y += self.speed

        self.rect.topleft = (self.x, self.y)


class Food:
    def __init__(self):
        self.kind = random.choice(['good', 'bad'])

        if self.kind == 'good' and GOOD_IMAGES:
            self.image = random.choice(GOOD_IMAGES)
        elif self.kind == 'bad' and BAD_IMAGES:
            self.image = random.choice(BAD_IMAGES)
        else:
            self.image = pygame.Surface((48, 48))
            self.image.fill(GREEN if self.kind == 'good' else RED)

        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 4 + score * 0.1
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))



# Инициализация игры
clock = pygame.time.Clock()
running = True
cat = Cat()

food_timer = 0
foods = []
score = 10

eaten_good = 0
happiness = 3
omnomnometr = []


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

    # Генерация новой еды
    food_timer -= dt
    if food_timer <= 0:
        foods.append(Food())
        min_delay = max(0.2, 2 - score * 0.05)
        food_timer = random.uniform(min_delay, min_delay + 0.5)

    # Обработка еды
    for food in foods:
        food.move()
        food.draw(WIN)

        # Проверка столкновения с котом
        if food.rect.colliderect(cat.rect):
            if food.kind == 'good':
                score += 1
                omnomnometr.append(food.image)
                eaten_good += 1
                # Бонус за каждые 10 хороших продуктов
                if eaten_good % 10 == 0:
                    score += 10
            else:
                score -= 1
                happiness -= 1
                eaten_good = 0
                omnomnometr = []

            foods.remove(food)
        # Удаление еды за экраном
        elif food.x < -50:
            foods.remove(food)

    # Удаление еды за экраном (альтернативный способ)
    foods = [food for food in foods if food.x + food.image.get_width() > 0]

    # Отрисовка интерфейса
    ui_font = pygame.font.SysFont(FONT, 28)

    # История съеденной еды
    for i, img in enumerate(omnomnometr[-10:]):
        WIN.blit(pygame.transform.scale(img, (32, 32)), (10 + i * 30, 10))

    # Счет и уровень счастья
    WIN.blit(ui_font.render(f'Счет: {score}', True, WHITE), (WIDTH // 2 - 50, 10))
    WIN.blit(ui_font.render(f'Счастье: {happiness}', True, WHITE), (WIDTH - 150, 10))
    # Обновление экрана
    pygame.display.update()

pygame.quit()