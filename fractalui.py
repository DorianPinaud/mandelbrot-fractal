# handle UI usage
# Dorian Pinaud
# 26/12/2017

from Tkinter import *
from mandelbrot import *
import ttk

padding = 20
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

    def generate_fractal_callback(self, event):
        self.mandelbrot_frame.drawing_index = 0
        nb_iteration = int(self.iteration_spinbox.get())
        self.mandelbrot_frame = MandelBrotFrame(self.mandelbrot_label_frame,
                                                Frame2D(self.w, self.h),
                                                nb_iteration,
                                                self.enable_computation)
        self.mandelbrot_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        

    def enable_computation(self, enable):
        self.compute_button.config(state="normal" if enable else "disabled")
        
    def initialize(self):
        self.grid()
        self.mandelbrot_label_frame = LabelFrame(self, text="Fractal view")
        self.mandelbrot_label_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        self.mandelbrot_frame = MandelBrotFrame(self.mandelbrot_label_frame,
                                                Frame2D(self.w, self.h),
                                                nb_iteration,
                                                self.enable_computation)
        self.mandelbrot_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        self.options_label_frame = LabelFrame(self, text="Fractal options")
        self.options_label_frame.grid(column = 1, row = 0, padx = padding, pady = padding)
        self.iteration_label_frame = LabelFrame(self.options_label_frame, text="iteration parameter")
        self.iteration_label_frame.grid(column = 0, row = 0, padx = padding, pady = padding)
        self.iteration_spinbox = Spinbox(self.iteration_label_frame, from_=1, to=50)
        self.iteration_spinbox.grid(column = 0, row = 1, padx = padding, pady = padding)
        self.compute_button = Button(self.options_label_frame, text="Compute")
        self.compute_button.grid(column = 0, row = 2, padx = padding, pady = padding)
        self.compute_button.bind("<Button-1>", self.generate_fractal_callback)
        
class MandelBrotFrame(Canvas):

    def __init__(self, parent, frame_2d, nb_iteration, enable_computation_callback):
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
        self.drawing_index = 0
        self.after(0, self.generate_view)
        self.enable_computation_callback = enable_computation_callback

    def generate_view(self):
        if self.drawing_index == 0:
            self.progressbar_view["value"] = 0
            self.progressbar_view.grid(column = 0, row = 0)
            self.enable_computation_callback(False)
        size = self.mandelbrot.w() * self.mandelbrot.h()
        for _ in range(0, self.mandelbrot.w()):
            x, y = self.drawing_index % self.mandelbrot.w(), self.drawing_index / (self.mandelbrot.w())
            color = "#{0:02x}{1:02x}{2:02x}".format(
                int(self.mandelbrot.point(x, y, self.nb_iteration).ratio * 255), 0, 0)
            self.img.put(color, (x, y))
            self.drawing_index += 1
            self.progressbar_view["value"] += 1
        if self.drawing_index <= size:
            self.after(1, self.generate_view)
        else:
            self.progressbar_view.grid_forget()
            self.enable_computation_callback(True)
