import math
import numpy as np


def mandelbrot(z, c, n=40):
    if abs(z) > 1000:
        return float("nan")
    elif n > 0:
        return mandelbrot(z ** 2 + c, c, n - 1)
    else:
        return z ** 2 + c


def gen_mandelbrot_arr():
    ar = np.zeros((40, 110))
    for k, y in enumerate([a * 0.05 for a in range(-20, 20)]):
        for n, x in enumerate([a * 0.02 for a in range(-80, 30)]):
            if not math.isnan(mandelbrot(0, x + 1j * y).real):
                ar[k, n] = 1

    mbrot = np.zeros((110, 110))
    for i in range(40):
        for j in range(110):
            mbrot[i + 35, j] = ar[i, j]
    return mbrot
