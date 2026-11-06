import tkinter as tk
import random

WIDHT= 400
HEIGTH = 400
DIRECTIONS = ['Up', 'Down', 'Left', 'Right']
CELL_SIZE = 10
DELAY = 100 # Скорость игры
root = tk.Tk()
root.title('Змейка | Счет: 0')
root.resizable(False, False)


canvas = tk.Canvas(
    root,
    width=WIDHT,
    height=HEIGTH,
    bg='black',
    highlightthickness=0 # Убираем границу
)
canvas.pack()


# Создаем стартвую змейку
def create_snake():
    # Определяем допустимый диапазон координат головы змейки
    max_x = (WIDHT // CELL_SIZE) - 3
    max_y = (HEIGTH // CELL_SIZE) - 1

    # Случайные координаты головы
    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE

    # Строим змейку из 3 сегментов, направленную вправо
    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]

snake = create_snake()
direction = 'Right'
score = 0
game_over = False


# Еда
def create_food():
    while True:
        x = random.randint(0, (WIDHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake: # Проверяем, не находится ли еда внутри змейки
            return (x, y)


def draw_food():
    canvas.create_rectangle(
        food[0], food[1],       # Верхрий левый угол
        food[0] + CELL_SIZE,    # x - координата правого края
        food[1] + CELL_SIZE,    # y - координата нижнего края
        fill='red',
    )

food = create_food()


# Отрисовка змейки
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],         # Верхний левый угол
            segment[0] + CELL_SIZE,         # Нижний правый угол (х)
            segment[1] + CELL_SIZE,         # Нижний правый угол (у)
            fill='green',
            outline='darkgreen'             # Цвет обводки        
        )


# Обработка клавиш
def on_key_pressed(event):
    global direction
    key = event.keysym

    # Управление направлением
    if key in DIRECTIONS and not game_over:
        # Запрещаем поворот в противоположную сторону
        if (key == 'Up' and direction != 'Down' or
            key == 'Down' and direction != 'Up' or
            key == 'Left' and direction != 'Right' or
            key == 'Right' and direction != 'Left'):
            direction = key

    # Перезапуск игры
    elif key == 'space' and game_over:
        restart_game()

root.bind('<KeyPress>', on_key_pressed)

# Движение змейки
def move_snake():
    head_x, head_y = snake[0]

    if direction == 'Up':
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == 'Down':
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == 'Left':
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == 'Right':
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0, new_head)           # Добавляем новую голову
    if not check_food_collision():      # Если еда не съедена
        snake.pop()                     # Удаляем хвост (если еда не съедена)


# Обновляем заголовок окна
def update_title():
    root.title(f'Snake | {score}')

# Проверка на поедание еды
def check_food_collision():
    global food, score
    if snake[0] == food:
        score += 1
        food = create_food()
        return True
    return False                    # Еда не съедена

# Проверяем столкновение со стенами
def check_wall_collision():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDHT or
        head_y < 0 or head_y >= HEIGTH
    )


# Проверяем столкновение с собой
def check_self_collision():
    return snake[0] in snake[1:]


# Рестарт игры
def restart_game():
    global snake, direction, food, score, game_over

    snake = create_snake()
    direction = "Right"
    food = create_food()
    score = 0
    game_over = False

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)

# Завершаем игру
def end_game():
    global game_over
    game_over = True
    canvas.create_text(
        WIDHT // 2, HEIGTH // 2,
        text=f'Game over! Score: {score}',
        fill='white',
        font=('Arial', 24)
    )


# Игровой цикл
def game_loop():
    global snake, food, score

    if game_over:
        return
    move_snake()

    if check_wall_collision() or check_self_collision():
        end_game()
        return
    
    canvas.delete('all')            # Очищаем холст
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)    # Повторяем через DELAY мс    


# Первоначальная отрисовка
draw_food()
draw_snake()
root.after(DELAY, game_loop)

# Запуск главного цикла
root.mainloop()