# test env

from mandelbrot import *
from fractalui import *
from PIL import Image, ImageColor

nb_iteration = 20
w = 36
h = 26
fractal = MandelBrotFrame(Frame2D(w, h), nb_iteration)
image = Image.new("RGB", (w, h), "white")
for y in range(0, fractal.h()):
    for x in range(0, fractal.w()):
        r  = fractal.point(x, y).ratio
        image.putpixel((x, y), (int(r * 125), int(r * 125), int(r * 125)))
image.save("fractal.png")

view = FractalUI()
