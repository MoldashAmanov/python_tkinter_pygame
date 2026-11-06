import tkinter as tk

def get_entry():
    value = name.get()
    if value:
        print(value)
    else:
        print('empty entry')


def delete_entry():
    name.delete(0, tk.END)


def submit():
    print(name.get())
    print(password.get())

win = tk.Tk()
win.geometry('400x600')
win.title('gui')
tk.Label(win, text='name').grid(row=0, column=0)
tk.Label(win, text='password').grid(row=1, column=0)
name = tk.Entry(win)
password = tk.Entry(win, show='*')
name.grid(row=0, column=1)
password.grid(row=1, column=1)
tk.Button(win, text='get', command=get_entry).grid(row=2, column=0)
tk.Button(win, text='delete', command=delete_entry).grid(row=2, column=1)
tk.Button(win, text='submit', command=submit).grid(row=3, column=0)
tk.Button(win, text='insert', command=lambda: name.insert(0, 'hello')).grid(row=2, column=2)


win.mainloop()