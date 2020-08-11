from tkinter import Tk, Button, Label
import ctypes
#from tkinter.ttk import *

# CLICKED HANDLER
def clicked():
    btn.configure(text="114514")
    lbl.configure(text="1919810")
    ctypes.windll.user32.MessageBoxW(None, '你是114514吗？', '恶臭测试', 1)

# CREATE A 320x240 WINDOW
top = Tk()
top.geometry("320x240")
# Add a button to the window
btn = Button(top,text="点我变成H O M O",command=clicked, width=30)
btn.grid(column=0, row=0)
btn.focus()
# Add a label
lbl = Label(top,text="")
lbl.grid(column=0, row=1)

# RUN WINDOW
top.mainloop()