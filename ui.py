from tkinter import *
class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("FaceRunner")
        self.root.geometry("500x500")
        self.startBuild()

    def startBuild(self):
        self.b1=Button(self.root,text='bt1',bd=1,width=10)
        self.b1.place(x=95,y=30)
        self.b2=Button(self.root,text='bt2',bd=1,width=10)
        self.b2.place(x=220,y=30)
        self.b3=Button(self.root,text='bt3',bd=1,width=10)
        self.b3.place(x=345,y=30)
        self.cb1=Checkbutton(self.root,text="I'm Sb",width=10,height=5,offvalue=1,onvalue=0)
        self.cb1.place(x=80,y=400)
        self.cb2=Checkbutton(self.root,text="I'm Siht",width=10,height=5,offvalue=1,onvalue=0)
        self.cb2.place(x=205,y=400)
        self.cb3=Checkbutton(self.root,text="I'm Fcuk",width=10,height=5,offvalue=1,onvalue=0)
        self.cb3.place(x=330,y=400)
        
    def run(self):
        self.root.mainloop()
