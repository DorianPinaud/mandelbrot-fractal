# handle UI usage
# Dorian Pinaud
# 26/12/2017

from Tkinter import *
from mandelbrot import *
import ttk

nb_iteration = 20
w = 720
h = 510

class FractalUI(Tk):

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.w = w
        self.h = h
        self.initialize()
        
    def initialize(self):
        padding = 20
        self.grid()
        self.mandelbrot_label_frame = LabelFrame(self, text="Fractal view")
        self.mandelbrot_label_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        self.mandelbrot_frame = MandelBrotFrame(self.mandelbrot_label_frame,
                                                Frame2D(self.w, self.h), nb_iteration)
        self.mandelbrot_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        self.options_label_frame = LabelFrame(self, text="Fractal options")
        self.options_label_frame.grid(column = 1, row = 0, padx = padding, pady = padding)
        self.compute_button = Button(self.options_label_frame, text="Compute")
        self.compute_button.grid(column = 0, row = 0, padx = padding, pady = padding)

class MandelBrotFrame(Canvas):

    def __init__(self, parent, frame_2d, nb_iteration):
        Canvas.__init__(self, parent)
        self.parent = parent
        self.nb_iteration = nb_iteration
        self.mandelbrot = MandelBrot(frame_2d)
        self.canvas = Canvas(self,
                             width = self.mandelbrot.w(),
                             height = self.mandelbrot.h(),
                             background='black')
        self.img = PhotoImage(width=self.mandelbrot.w(), height=self.mandelbrot.h())
        self.canvas.create_image((self.mandelbrot.w() / 2, self.mandelbrot.h() / 2),
                                 image=self.img,
                                 state="normal")
        self.canvas.grid(column = 0, row = 0)
        self.progressbar_view = ttk.Progressbar(orient=HORIZONTAL,
                                                maximum= self.mandelbrot.h() * self.mandelbrot.w(),
                                                length=250,
                                                mode="determinate")
        self.progressbar_view.grid(column = 0, row = 1)        
        self.drawing_index = 0
        self.after(0, self.generate_view)
        
        
    def generate_view(self):
        size = self.mandelbrot.w() * self.mandelbrot.h()
        for _ in range(0, self.mandelbrot.w()):
            x, y = self.drawing_index % self.mandelbrot.w(), self.drawing_index / (self.mandelbrot.w())
            self.img.put("#{0:02x}{1:02x}{2:02x}".format(
                int(self.mandelbrot.point(x, y, self.nb_iteration).ratio * 255), 0, 0), (x, y))
            self.drawing_index += 1
            self.progressbar_view["value"] += 1        
        if self.drawing_index <= size:
            self.after(1, self.generate_view)
        else:
            self.progressbar_view.grid_forget()

