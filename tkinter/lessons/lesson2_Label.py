import tkinter as tk

win = tk.Tk()
win.geometry('300x400')
win.title('first gui')
label_1 = tk.Label(win, text='labelOne',
                   bg='black',
                   fg='white',
                   font=('Arial', 20, 'bold'),
                   # padx=10,
                   # pady=20
                   width=15,
                   height=4,
                   anchor='n',
                   relief=tk.RAISED,
                   bd=10,
                   justify=tk.LEFT)
label_1.pack()


win.mainloop()