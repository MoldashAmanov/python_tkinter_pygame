import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

root = tk.Tk()
# root.geometry('400x400')
root.title('tictactoe')

icon = PhotoImage(file='image.png')
root.iconphoto(False, icon)

buttons = []            # Храним все кнопки
current_player = 'X'
game_over = False

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтальные линии
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикальные линии
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        a, b, c = combo
        if buttons[a]['text'] == buttons[b]['text'] == buttons[c]['text'] != '':
            buttons[a]['highlightbackground'] = 'lightgreen'
            buttons[b]['highlightbackground'] = 'lightgreen'
            buttons[c]['highlightbackground'] = 'lightgreen'
            return True
    return False


def on_click(index):
    global current_player, game_over
    if game_over:
        return
    if buttons[index]['text'] == '':
        buttons[index]['text'] = current_player

        # Проверяем, есть ли победитель
        if check_winner():
            game_over = True
            messagebox.showinfo('Победа!', f'Победил {current_player}')
        elif all(button['text'] != '' for button in buttons):   # Проверяем ничью
            game_over = True
            messagebox.showinfo('Ничья!', 'Игра окончена!')
        else:
            # Меняем игрока
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'


def reset_game():
    global current_player, game_over
    current_player = 'X'
    game_over = False

    # Очищаем все кнопки, возвращая стандартный цвет и убираем текст
    for button in buttons:
        button.config(text='', bg=default_button_color)


for i in range(9):      # Создаем 9 кнопок
    button = tk.Button(
        root,
        text='',
        font=('Arial', 30),
        width=5,
        height=2,
        command=lambda idx = i: on_click(idx)
    )
    button.grid(row=i//3, column=i%3)   # Размещаем кнопку в сетке
    buttons.append(button)              # Добавляем кнопку в список


# Запоминаем стандартный цвет кнопок
default_button_color = buttons[0].cget('bg')

# Создание кнопки сброса
reset_button = tk.Button(root, text='Новая игра', font=('Arial', 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, sticky='we')



root.mainloop()