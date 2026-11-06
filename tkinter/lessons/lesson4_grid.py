import tkinter as tk
win = tk.Tk()

win. geometry('400x600')
win.title('first app gui')
btn1 = tk.Button(win, text='btn1')
btn2 = tk.Button(win, text='btn2')
btn3 = tk.Button(win, text='btn3')
btn4 = tk.Button(win, text='btn4')
btn5 = tk.Button(win, text='btn5')
btn6 = tk.Button(win, text='btn6')
btn7 = tk.Button(win, text='btn7')
btn8 = tk.Button(win, text='btn8')

btn1.grid(row=0, column=0)
btn2.grid(row=0, column=1)
btn3.grid(row=1, column=0)
btn4.grid(row=1, column=1)
btn5.grid(row=2, column=0)
btn6.grid(row=2, column=1)
btn7.grid(row=3, column=0, columnspan=2, stick='we')
btn8.grid(row=0, column=2, rowspan=4, stick='ns')

win.mainloop()