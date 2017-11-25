import csv
from random import shuffle, randint
import numpy as np
from matplotlib import pyplot as plt

file = 'sudoku.csv'

size = 9


def read():
    res = np.zeros((size, size))
    can_change = np.zeros((size, size), dtype=np.bool_)
    with open(file) as sudoku_csv:
        reader = csv.reader(sudoku_csv, delimiter=';')
        for i, row in enumerate(reader):
            for j, num in enumerate(row):
                if num is not 'x':
                    res[i][j] = int(num)
                else:
                    can_change[i][j] = True
    return res, can_change


def count_matrix_energy(map):
    results = np.zeros(size, dtype=int)
    for i in np.nditer(map):
        results[int(i - 1)] += 1
    return sum([x - 1 for x in results if x > 1])

def count_matrix_enhergy(map):
    results = np.zeros(size, dtype=int)
    for i in np.nditer(map):
        results[int(i - 1)] += 1
    energy =  sum([x - 1 for x in results if x > 1])

class Sudoku(object):
    def __init__(self):
        self.map, self.can_change = read()
        self.energy = []
        self.recently_swaped = None

    def generate_random_solution(self):
        nums = np.ones(9, dtype=int) * 9
        for i in np.nditer(self.map):
            if i != 0:
                nums[int(i - 1)] = nums[int(i - 1)] - 1
        numbers_to_insert = []
        for i, num in enumerate(nums):
            for j in range(num):
                numbers_to_insert.append(i + 1)
        shuffle(numbers_to_insert)
        for i in range(size):
            for j in range(size):
                if self.map[i][j] == 0:
                    self.map[i][j] = numbers_to_insert[0]
                    numbers_to_insert.pop(0)
        self.energy.append(self.count_energy())

    def count_energy(self):
        small_size = int(np.sqrt(size))
        energy = 0
        for i in range(small_size):
            for j in range(small_size):
                energy += count_matrix_energy(self.map[i:i + small_size, j:j + small_size])
        for row in self.map:
            energy += count_matrix_energy(row)
        for column in self.map.T:
            energy += count_matrix_energy(column)
        return energy

    def swap_random(self):
        p1_x, p1_y = randint(0, size - 1), randint(0, size - 1)
        p2_x, p2_y = randint(0, size - 1), randint(0, size - 1)
        while not self.can_change[p1_x][p1_y]:
            p1_x, p1_y = randint(0, size - 1), randint(0, size - 1)
        while not self.can_change[p2_x][p2_y]:
            p2_x, p2_y = randint(0, size - 1), randint(0, size - 1)
        self.map[p1_x][p1_y], self.map[p2_x][p2_y] = self.map[p2_x][p2_y], self.map[p1_x][p1_y]
        self.recently_swaped = ((p1_x, p1_y), (p2_x, p2_y))
        self.energy.append(self.count_energy())

    def reswap(self):
        (p1_x, p1_y), (p2_x, p2_y) = self.recently_swaped
        self.map[p1_x][p1_y], self.map[p2_x][p2_y] = self.map[p2_x][p2_y], self.map[p1_x][p1_y]
        self.energy.pop()

    def draw(self):
        print(self.map)
        if len(self.energy) > 1:
            plt.plot(range(len(self.energy)), self.energy)
            plt.show()


x = Sudoku()
x.generate_random_solution()
print(x.count_energy())
