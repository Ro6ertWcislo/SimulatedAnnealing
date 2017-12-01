"""
This module can be used to generate points on a map.
Then the random path going through all of the points can be generated.
That means it produces input for simulated annealing algorithm
"""

import math
from random import randint, shuffle
from matplotlib import pyplot as plt


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return "x: {}, y: {} ".format(self.x, self.y)


class Path(object):
    def __init__(self):
        self.path = []
        self.energy = []
        self.recently_swaped = None

    def clear(self):
        self.path, self.energy, self.recently_swaped = [], [], None

    def generate_uniform(self, size, bound):
        self.clear()
        self.path = [Point(randint(0, bound), randint(0, bound)) for i in range(size)]
        self.size = len(self.path)
        self.energy.append(self.count_energy())

        x = [p.x for p in self.path]
        y = [p.y for p in self.path]
        plt.plot(x, y)
        plt.show()

    def generate_simple(self, size):
        self.clear()
        for i in range(size):
            self.path.append(Point(10, i * 10))
        for i in range(size):
            self.path.append(Point(i * 10 + 10, size * 10))
        for i in range(size):
            self.path.append(Point(i * 10 + 10, 10))
        for i in range(size):
            self.path.append(Point(size * 10, i * 10))
        shuffle(self.path)
        self.size = len(self.path)
        self.energy.append(self.count_energy())
        x = [p.x for p in self.path]
        y = [p.y for p in self.path]
        plt.plot(x, y)
        plt.show()

    def generate_clusters(self, clusters, node_per_cluster):
        self.clear()
        for i in range(clusters ** 4):
            for k in range(clusters ** 4):
                if k % clusters ** 3 == 0 and i % clusters ** 3 == 0:
                    for j in range(node_per_cluster):
                        self.path.append(Point(randint(k * node_per_cluster, (k + 1) * node_per_cluster - 1),
                                               randint(i * node_per_cluster, (i + 1) * node_per_cluster - 1)))
        shuffle(self.path)
        self.size = len(self.path)
        self.energy.append(self.count_energy())
        x = [p.x for p in self.path]
        y = [p.y for p in self.path]
        plt.plot(x, y)
        plt.show()

    def draw(self):
        x = [p.x for p in self.path]
        y = [p.y for p in self.path]
        plt.plot(x, y)
        plt.show()

        plt.plot(range(len(self.energy)), self.energy)
        plt.show()

    def swap_random(self):
        p1 = randint(0, self.size - 1)
        p2 = p1
        while p1 == p2:
            p2 = randint(0, self.size - 1)
        energy = self.energy[-1] - self.energy_delta(p1, p2)
        self.path[p1], self.path[p2] = self.path[p2], self.path[p1]
        self.energy.append(
            energy + self.energy_delta(p1, p2))
        self.recently_swaped = (p1, p2)

    def swap_neighbour(self):
        p1 = randint(0, self.size - 1)
        p2 = (p1 + 1) % self.size
        energy = self.energy[-1] - self.energy_delta(p1, p2)
        self.path[p1], self.path[p2] = self.path[p2], self.path[p1]
        self.energy.append(
            energy + self.energy_delta(p1, p2))
        self.recently_swaped = (p1, p2)

    def reswap(self):
        p1, p2 = self.recently_swaped
        self.path[p1], self.path[p2] = self.path[p2], self.path[p1]
        self.energy.pop()

    def count_energy(self):
        energy = 0
        for i in range(self.size):
            energy += self.path[i].dist(self.path[(i + 1) % self.size])
        return energy

    def energy_delta(self, p1, p2):
        e_p1 = self.path[(len(self.path) + p1 - 1) % len(self.path)].dist(self.path[p1]) + \
               self.path[(len(self.path) + p1 + 1) % len(self.path)].dist(self.path[p1])
        e_p2 = self.path[(len(self.path) + p2 - 1) % len(self.path)].dist(self.path[p2]) + \
               self.path[(len(self.path) + p2 + 1) % len(self.path)].dist(self.path[p2])
        return e_p1 + e_p2
