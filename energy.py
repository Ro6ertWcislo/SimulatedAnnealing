"""
This module contains energy functions and neighbourhood types to be used by bitmap module
"""

import numpy as np
from mandelbrot import gen_mandelbrot_arr


def weird_energy(x,y,map,size):
    return 17**2 - (np.math.sqrt((x-size/2)**2 + (y-size/2)**2)//5 + (0 - map[(x + 1) % size][y] - map[(x + 1) % size][(y + 1) % size] - map[x][(y + 1) % size] -
                    map[(x - 1) % size][(y + 1) % size] -
                    map[(x - 1) % size][y] - map[(x - 1) % size][(y - 1) % size] - map[x][(y - 1) % size] -
                    map[(x + 1) % size][(y - 1) % size])**2)

mandelbrot = gen_mandelbrot_arr()


def mandelbrot_energy(x, y, map, size):
    if map[x, y]:

        if mandelbrot[x, y] == 1.0:
            return 0
        else:
            return np.math.sqrt((x - 55) ** 2 + (y - 55) ** 2)
    else:
        if mandelbrot[x, y] == 1.0:
            return np.math.sqrt((x - 55) ** 2 + (y - 55) ** 2)
        else:

            return 0


def mandelbrot_neighbours(x, y, map, size):
    return []


def eight_friends_neighbours(x, y, map, size):
    tmp = [((x + 1) % size, y), ((x + 1) % size, (y + 1) % size), (x, (y + 1) % size),
           ((x - 1) % size, (y + 1) % size),
           ((x - 1) % size, y), ((x - 1) % size, (y - 1) % size), (x, (y - 1) % size),
           ((x + 1) % size, (y - 1) % size)]
    return [(x, y) for x, y in tmp if map[x][y]]


def eight_friends_energy(x, y, map, size):
    """ the more neighbours your have, the least energy you have. The lesser energy, the better"""
    return 8 - (0 - map[(x + 1) % size][y] - map[(x + 1) % size][(y + 1) % size] - map[x][(y + 1) % size] -
                map[(x - 1) % size][(y + 1) % size] -
                map[(x - 1) % size][y] - map[(x - 1) % size][(y - 1) % size] - map[x][(y - 1) % size] -
                map[(x + 1) % size][(y - 1) % size])


def double_energy(x, y, map, size):
    return 16 - (sum([map[(x + i) % size][y + j] for i in [-2, -1, 0, 1, 2] for j in [2, -2]]) +
                 sum([map[(x + i) % size][y + j] for i in [-2, 2] for j in [1, 0, -1]])
                 - eight_friends_energy(x, y, map, size))


def double_neighbours(x, y, map, size):
    tmp = (eight_friends_neighbours(x, y, map, size) +
           [((x + i) % size, y + j) for i in [-2, -1, 0, 1, 2] for j in [2, -2]] +
           [((x + i) % size, y + j) for i in [-2, 2] for j in [-1, 0, 1]])
    return [(x, y) for x, y in tmp if map[x][y]]


def nine_friends_energy(x, y, map, size):
    """ the more neighbours your have, the least energy you have. The lesser energy, the better"""
    x = (map[(x + 1) % size][(y + 1) % size] + map[(x + 1) % size][(y - 1) % size] + map[(x + 2) % size][y])

    return 9 - x ** 2


def nine_friends_neighbours(x, y, map, size):
    tmp = [((x + 1) % size, (y + 1) % size),
           ((x + 1) % size, (y - 1) % size), ((x + 2) % size, y)]
    return [(x, y) for x, y in tmp if map[x][y]]


def four_friends_neighbours(x, y, map, size):
    tmp = [((x + 1) % size, y), (x, (y + 1) % size),
           ((x - 1) % size, y), (x, (y - 1) % size)]
    return [(x, y) for x, y in tmp if map[x][y]]


def four_friends_energy(x, y, map, size):
    """ the more neighbours your have, the least energy you have. The lesser energy, the better"""
    x = 16 - (0 - map[(x + 1) % size][y] - map[x][(y + 1) % size] -
              map[(x - 1) % size][y] - map[x][(y - 1) % size]) ** 2
    return np.math.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2) / 2 + x


def diagonal_energy(x, y, map, size):
    if map[x][y]:
        return ((x - y) ** 2) / 2
    else:
        return size ** 2


def diagonal_neighbours(x, y, map, size):
    return []


def even_energy(x, y, map, size):
    if x % 2 == 0 and y % 2 == 0 and map[x][y]:
        return 0
    else:
        return size


def even_neighbours(x, y, map, size):
    return [(i, j) for i, j in [((x + 1) % size, y), ((x - 1) % size, y), (x, (y + 1) % size), (x, (y - 1) % size)] if
            map[i][j]]
