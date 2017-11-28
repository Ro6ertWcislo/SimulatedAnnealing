import numpy as np
from model import Path
from matplotlib import pyplot as plt
import random


def choose_state(T, energy_prev, energy_act):
    try:
        p = np.math.exp((energy_prev - energy_act) / T)
    except:
        p = 1
    if energy_act < energy_prev:
        return energy_act
    else:
        if random.random() < p:
            return energy_act
        else:
            return energy_prev


def solve(path, temp_space):
    for T in temp_space:
        path.swap_random()
        energy_prev, energy_act = path.energy[-2:]
        energy_chosen = choose_state(T, energy_prev, energy_act)
        if energy_chosen == energy_prev:
            path.reswap()

    print(len(path.energy))
    return path

#
# from bitmap import *
# x = BitMap()
# x.set_energy_and_neighbourhood(mandelbrot_energy, mandelbrot_neighbours)
# x.generate_with_density(110,0.3)
# x.dot_size=30
# x.draw()
# solve(x,np.logspace(3, -2, 1000000))
# x.draw()
# plt.plot(range(len(x.energy)), x.energy)
# plt.show()
# print(x.energy)

from sudoku import Sudoku



su =Sudoku()
su.generate_random_solution()
solve(su, np.logspace(2,-3,100000))


