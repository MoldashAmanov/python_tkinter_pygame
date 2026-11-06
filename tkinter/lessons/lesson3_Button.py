import tkinter as tk


def sayHello():
    print('hi')

def add_label():
    label = tk.Label(win, text='new')
    label.pack()

count = 0

def counter():
    global count
    count += 1
    btn4['text'] = f'counter {count}'

win = tk.Tk()
win.geometry('500x800')
win.title('first gui')
btn1 = tk.Button(win, text='hello',
                 command=sayHello)
btn1.pack()

btn2 = tk.Button(win, text='hi', 
                command=add_label)
btn2.pack()

btn3 = tk.Button(win, text='add third button',
                command=lambda: tk.Label(win, text='textLamda').pack())
btn3.pack()

btn4 = tk.Button(win, text=f'counter {count}',
                command=counter,
                activebackground='blue',
                bg='red',
                #state=tk.DISABLED
                )
btn4.pack()
win.mainloop()