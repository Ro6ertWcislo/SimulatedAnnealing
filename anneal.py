""""
Implementation of simulated annealing.
temp_space is an array of temperatures, you can pass e.i. np.logspace(4,-1,100000)
path must be a class implementing methods: swap_random or swap_neighbour, reswap, and must have an energy array
"""

import numpy as np
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


def solve_random(path, temp_space):
    for T in temp_space:
        path.swap_random()
        energy_prev, energy_act = path.energy[-2:]
        energy_chosen = choose_state(T, energy_prev, energy_act)
        if energy_chosen == energy_prev:
            path.reswap()
    return path


def solve_neighbour(path, temp_space):
    for T in temp_space:
        path.swap_neighbour()
        energy_prev, energy_act = path.energy[-2:]
        energy_chosen = choose_state(T, energy_prev, energy_act)
        if energy_chosen == energy_prev:
            path.reswap()
    return path
