import tkinter as tk
from PIL import Image, ImageTk

win = tk.Tk()
win.title("tkinter app")

win.geometry('600x700+100+250') # размер при создании и расположение
win.resizable(True, True) # разрешение на изменение окна
# win.minsize(300, 400) # минимальное изменение 
# win.maxsize(800, 1000) # максимальное изменение
win.config(bg='yellow')
image = Image.open('fun.jpg')
photo = ImageTk.PhotoImage(image)
win.iconphoto(False, photo)
win.mainloop()