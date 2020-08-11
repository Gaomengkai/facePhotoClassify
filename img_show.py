from PIL import ImageTk,Image
from tkinter import Tk,Label

def showImageOnTk(img:Image.Image):
    top = Tk()
    tkimg = ImageTk.PhotoImage(img)
    label = Label(top,image=tkimg)
    label.pack()
    top.mainloop()
