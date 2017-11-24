import numpy as np
from model import Path
from matplotlib import pyplot as plt
import random


def choose_state(T, energy_prev, energy_act):
    p = np.math.exp((-1) * (energy_act - energy_prev) / T)
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


path2 = Path()
path2.generate_simple(15)

solve(path2, np.logspace(4, 0, 10000))
plt.figure(figsize=(8, 4))

xx = [p.x for p in path2.path] + [path2.path[0].x]

y = [p.y for p in path2.path] + [path2.path[0].y]
plt.plot(xx, y)

#
plt.show()

plt.figure(figsize=(16, 8))
plt.plot(range(len(path2.energy)), path2.energy)

plt.show()
print("done")
