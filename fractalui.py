from Tkinter import *

class FractalUI:

    def __init__(self):
        self.window = Tk()
        
        self.title = Label(self.window, text="Fractal Manager")
        self.title.pack()
        self.window.mainloop()
