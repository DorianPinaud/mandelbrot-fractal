# compute mandelbrot fractal point
# Dorian Pinaud
# 23/12/2017

import math

class Complex:

    def __init__(self, r, i):
        self.r = r
        self.i = i
        self.m = self.module()

    def __str__(self):
        s = "({0},{1})".format(self.r, self.i)
        return s
        
    def module(self):
        return math.sqrt(self.r * self.r + self.i * self.i)
    
class MandelBrotPnt:
    
    def __init__(self, c, nb_iteration):
        self.c = c
        z = Complex(0, 0)
        iteration = 0
        while iteration < nb_iteration and z.module() < 2:
            tmp = z.r
            z.r = z.r * z.r - z.i * z.i + c.r
            z.i = 2 * tmp * z.i + c.i
            iteration += 1
        self.module = z.module()
        self.iteration = float(iteration)
        self.nb_iteration = float(nb_iteration)
        self.is_bounded = iteration == nb_iteration
        self.ratio = self.iteration / self.nb_iteration

    def r(self):
        return self.c.r

    def i(self):
        return self.c.i

    def m(self):
        return self.c.m

    def __str__(self):
        s = "+" if self.is_bounded else "-"
        return s
    
class Frame2D:

    def __init__(self, w, h):
        self.w = w
        self.h = h     
        self.indices = [(i % (w + 1), (i / (w + 1))) for i in range(0, (w + 1) * (h + 1))]
        self.x_indices, self.y_indices = zip(*self.indices)

    def __str__(self):
        s = "Frame2D [\n"
        s += "\t- x indices : {0}\n".format(self.x_indices)
        s += "\t- y indices : {0}\n".format(self.y_indices)
        s += "\t- xy indices: {0}\n".format(zip(self.x_indices, self.y_indices))
        s += "]"
        return s


class MandelBrotFrame:

    def __init__(self, frame_2d, nb_iteration):
        self.cx = -2.1, 0.6
        self.cy = -1.2, 1.2
        self.nb_iteration = nb_iteration
        self.frame_2d = frame_2d
        self.zoom_w = frame_2d.w / (self.cx[1] - self.cx[0])
        self.zoom_h = frame_2d.h / (self.cy[1] - self.cy[0])
        self.indices_x = [i / self.zoom_w + self.cx[0] for i in self.frame_2d.x_indices]
        self.indices_y = [i / self.zoom_h + self.cy[0] for i in self.frame_2d.y_indices]
        self.indices = zip(self.indices_x, self.indices_y)
        self.c_indices = [Complex(i[0], i[1]) for i in self.indices]
        self.mandelbrot_points = [MandelBrotPnt(c, nb_iteration) for c in self.c_indices]

    def point(self, x, y):
        return self.mandelbrot_points[x + (y * (self.w() + 1))]

    def h(self):
        return self.frame_2d.h

    def w(self):
        return self.frame_2d.w
    
    def generate_(self, tab):
        s = ""
        for y in range(0, self.h()):
            for x in range(0, self.w()):
                s += str(tab[x + (y * (self.w() + 1))])
            s += "\n"
        return s
        
    def generate_fractal(self):    
        s = "Mandelbrot fractal:\n"
        s += self.generate_(self.mandelbrot_points)
        return s

    def generate_complex_space(self):
        s = "Complex space:\n"
        s += self.generate_(self.c_indices)
        return s
    
    def __str__(self):
        s = "Mandelbrot Frame [\n"
        s += "\t- x indices : {0}\n".format(self.indices_x)
        s += "\t- y indices : {0}\n".format(self.indices_y)
        s += "\t- complex indices: {0}\n".format([str(c) for c in self.c_indices])
        s += "\t- mandelbrot points: {0}\n".format([p.ratio_from_boundary for p in self.mandelbrot_points])
        s += "]"
        return s
