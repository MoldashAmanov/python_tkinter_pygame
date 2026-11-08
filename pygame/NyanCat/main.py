import pygame
import random
import os

# Инициализация
pygame.init()

# Модуль звуков
pygame.mixer.init()

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
    dummy_frame.fill(PINK)
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

# Загружаем звук
SOUND_EAT_GOOD = SOUND_EAT_BAD = SOUND_HAPPINESS_STAR = SOUND_GAME_OVER = SOUND_BG_MUSIC = None
try:
    SOUND_EAT_GOOD = pygame.mixer.Sound('sounds/eat_good.wav')
    SOUND_EAT_BAD = pygame.mixer.Sound('sounds/eat_bad.wav')
    SOUND_HAPPINESS_STAR = pygame.mixer.Sound('sounds/happiness_star.wav')
    SOUND_GAME_OVER = pygame.mixer.Sound('sounds/game_over.mp3')
    SOUND_BG_MUSIC = pygame.mixer.Sound('sounds/background_music.mp3')

    SOUND_BG_MUSIC.set_volume(0.1)
    SOUND_EAT_GOOD.set_volume(0.2)
except:
    print('Не удалось загрузить некоторые звуки')

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


class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 5)
        self.size = random.randint(1, 2)

    def move(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


class HappinessStar:
    def __init__(self):
        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 10
        self.size = 15
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size)
        pygame.draw.circle(surface, WHITE, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size // 2)


# Главное меню
def draw_main_menu():
    WIN.fill(DARK_BLUE)

    for star in stars:
        star.move()
        star.draw(WIN)

    title_font = pygame.font.SysFont(FONT, 64)
    button_font = pygame.font.SysFont(FONT, 36)

    title = title_font.render('Nyan Cat', True, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    start_text = button_font.render('Начать игру', True, DARK_BLUE)
    button_rect = pygame.Rect(WIDTH // 2 - 120, 300, 240, 60)
    pygame.draw.rect(WIN, YELLOW, button_rect, border_radius=12)
    WIN.blit(start_text, (button_rect.centerx - start_text.get_width() // 2,
                          button_rect.centery - start_text.get_height() // 2))

    pygame.display.update()
    return button_rect

# Перезапуск игры
def reset_game():
    global score, omnomnometr, happiness, eaten_good, food_timer, paused
    global game_over, foods, stars, happiness_stars, last_happiness_star, cat
    global high_score
    high_score = load_high_score()

    food_timer = 0
    foods = []
    score = 10
    eaten_good = 0
    happiness = 3
    omnomnometr = []
    stars = [Star() for _ in range(50)]
    happiness_stars = []
    last_happiness_star = pygame.time.get_ticks()
    paused = False
    game_over = False
    cat = Cat()

    try:
        SOUND_BG_MUSIC.stop()
        SOUND_BG_MUSIC.play(-1)
    except:
        pass

# Воспроизводим звуки
def play_sound(sound):
    try:
        sound.play()
    except:
        pass

# Сохраняем рекорд
def save_high_score(score): 
    with open('high_score.txt', 'w') as f:
        f.write(str(score))

# Загружаем рекорд
def load_high_score():
    if os.path.exists('high_score.txt'):
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    return 0

# Инициализация игры
clock = pygame.time.Clock()
running = True
menu = True

# Первоначальная настройка игры
reset_game()

# Главный игровой цикл
while running:
    current_time = pygame.time.get_ticks()
    dt = clock.tick(60) / 1000

    WIN.fill(DARK_BLUE)

    if menu:
        button_rect = draw_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu = False
                    reset_game()
        continue

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_SPACE and game_over:
                reset_game()

    # Обрабатываем режим паузы
    if paused:
        font = pygame.font.SysFont(FONT, 50)
        pause_text = font.render("Пауза", True, YELLOW)
        instruction_text = font.render("Нажмите ESC, чтобы продолжить", True, WHITE)

        WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 40))
        WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.update()
        continue

    # Обработка окончания игры
    if game_over:
        font1 = pygame.font.SysFont(FONT, 72)
        font2 = pygame.font.SysFont(FONT, 30)

        text = font1.render('Игра окончена!', True, RED)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 72))

        high_score_text = font2.render(f'Ваш счет: {score} | Рекорд: {high_score}', True, YELLOW)
        WIN.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 72))

        restart_text = font2.render('Нажмите ПРОБЕЛ для перезапуска', True, WHITE)
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 50))

        pygame.display.update()
        continue

    # Обновление состояния
    keys = pygame.key.get_pressed()

    # Рисуем звезды
    for star in stars:
        star.move()
        star.draw(WIN)

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

                play_sound(SOUND_EAT_GOOD)

                # Бонус за каждые 10 хороших продуктов
                if eaten_good % 10 == 0:
                    score += 10
                    play_sound(SOUND_HAPPINESS_STAR)
            else:
                score -= 1
                happiness -= 1
                eaten_good = 0
                omnomnometr = []

                play_sound(SOUND_EAT_BAD)

            foods.remove(food)
        # Удаление еды за экраном
        elif food.x < -50:
            foods.remove(food)

    # Удаление еды за экраном (альтернативный способ)
    foods = [food for food in foods if food.x + food.image.get_width() > 0]

    # Рисуем звезды счастья
    if current_time - last_happiness_star > random.randint(20000, 30000):
        happiness_stars.append(HappinessStar())
        last_happiness_star = current_time

    # Обработка звезд счастья
    for star in happiness_stars[:]:
        star.move()
        star.draw(WIN)

        if star.rect.colliderect(cat.rect):
            happiness = min(3, happiness + 1)
            happiness_stars.remove(star)
        elif star.x < -50:
            happiness_stars.remove(star)

    # Отрисовка интерфейса
    ui_font = pygame.font.SysFont(FONT, 28)

    # История съеденной еды
    for i, img in enumerate(omnomnometr[-10:]):
        WIN.blit(pygame.transform.scale(img, (32, 32)), (10 + i * 30, 10))

    # Счет и уровень счастья
    WIN.blit(ui_font.render(f'Счет: {score}', True, WHITE), (WIDTH // 2 - 50, 10))
    WIN.blit(ui_font.render(f'Счастье: {happiness}', True, WHITE), (WIDTH - 150, 10))
    
    # Проверяем условие окончания игры
    if (score < 1 or happiness <= 0) and not game_over:
        game_over = True

        try:
            SOUND_BG_MUSIC.stop()
        except:
            pass
        play_sound(SOUND_GAME_OVER)

        if score > high_score:
            high_score = score
            save_high_score(high_score)

    # Обновление экрана
    pygame.display.update()

pygame.quit()