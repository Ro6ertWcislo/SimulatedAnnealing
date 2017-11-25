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


# from bitmap import *
# x = BitMap()
# x.set_energy_and_neighbourhood(four_friends_energy,four_friends_neighbours)
# x.generate_with_density(128,0.2)
#
# x.draw()
# solve(x,np.logspace(5, -2, 10000000))
# x.draw()
# plt.plot(range(len(x.energy)), x.energy)
# plt.show()
# print("done")

from sudoku import Sudoku

x = Sudoku()
x.generate_random_solution()

solve(x, np.logspace(3,0,200000))
x.draw()
print(x.energy[-25:])

"""
ladne wyniki:
dla eight
x.generate_with_density(32,0.1)
solve(x,np.logspace(1, -1, 40000))




x.set_energy_and_neighbourhood(diagonal_energy,diagonal_neighbours)
x.generate_with_density(32,0.3)

x.draw()
solve(x,np.logspace(3.5, -1, 40000))

"""
