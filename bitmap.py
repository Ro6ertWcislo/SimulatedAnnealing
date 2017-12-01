import numpy as np
import random
from matplotlib import pyplot as plt


class BitMap(object):
    """
    Creates a bitmap, generates random point with given density.
    Implements methods needed by anneal.
    Usage:
    Generate bitmap, then pass energy function and neighbourhood type
    run solve_random from anneal and it will minimise your given energy function
    """
    def __init__(self):
        self.size = 0
        self.points = 0
        self.map = []
        self.energy = []
        self.recently_swaped = None
        self.energy_fun = None
        self.neighbour_fun = None
        self.dot_size = 6

    def set_energy_and_neighbourhood(self, energy_fun, neighbour_fun):
        self.energy_fun = energy_fun
        self.neighbour_fun = neighbour_fun

    def generate_with_density(self, size, density):
        self.size = size
        self.map = np.zeros((size, size), dtype=np.bool_)
        for i in range(size):
            for j in range(size):
                if random.random() < density:
                    self.map[i][j] = True
        self.energy.append(
            self.count_map_energy())

    def count_map_energy(self):
        energy = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j]:
                    energy += self.energy_fun(i, j, self.map, self.size)
        return energy

    def swap_random(self):
        p1_x, p1_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        p2_x, p2_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        energy = self.energy[-1] - self.energy_delta(((p1_x, p1_y), (p2_x, p2_y)))
        self.map[p1_x][p1_y], self.map[p2_x][p2_y] = self.map[p2_x][p2_y], self.map[p1_x][p1_y]
        self.energy.append(
            energy + self.energy_delta(((p1_x, p1_y), (p2_x, p2_y)))
        )
        self.recently_swaped = ((p1_x, p1_y), (p2_x, p2_y))

    def reswap(self):
        (p1_x, p1_y), (p2_x, p2_y) = self.recently_swaped
        self.map[p1_x][p1_y], self.map[p2_x][p2_y] = self.map[p2_x][p2_y], self.map[p1_x][p1_y]
        self.energy.pop()

    def draw(self):
        x_ax, y_ax = [], []
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j]:
                    x_ax.append(i)
                    y_ax.append(j)
        plt.figure(figsize=(16, 8))
        plt.scatter(x_ax, y_ax, marker='o', s=self.dot_size)
        plt.show()

        if len(self.energy) > 1:
            plt.plot(range(len(self.energy)), self.energy)
            plt.show()

    def energy_delta(self, recently_swaped):
        (p1_x, p1_y), (p2_x, p2_y) = recently_swaped
        x = self.energy_fun(p1_x, p1_y, self.map, self.size) + self.energy_fun(p2_x, p2_y, self.map,
                                                                               self.size)
        y = sum([self.energy_fun(x, y, self.map, self.size) for x, y in
                 self.neighbour_fun(p1_x, p1_y, self.map, self.size)])
        z = sum([self.energy_fun(x, y, self.map, self.size) for x, y in
                 self.neighbour_fun(p2_x, p2_y, self.map, self.size)])
        return x + y + z
