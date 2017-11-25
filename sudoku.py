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
    return sum([x - 1 for x in results if x > 1])**3


def count_matrix_enhergy(map):
    results = np.zeros(size, dtype=int)
    for i in np.nditer(map):
        results[int(i - 1)] += 1
    energy = sum([x - 1 for x in results if x > 1])


class Sudoku(object):
    def __init__(self):
        self.map, self.can_change = read()
        self.energy = []
        self.recently_swaped = None
        self.legal_columns = None

    def generate_random_solution(self):

        for col_num, column in enumerate(self.map.T):
            nums = np.zeros(9, np.bool_)
            for row_num, number in enumerate(column):
                if number > 0:
                    nums[int(number) - 1] = True
                    self.can_change[row_num][col_num] = False
            legal_vals = [x + 1 for x, occupied in enumerate(nums) if not occupied]
            if len(legal_vals) > 0:
                for row_num in range(size):
                    if self.map[row_num][col_num] == 0:
                        self.map[row_num][col_num] = legal_vals[0]
                        legal_vals.pop(0)
        self.assign_legal_columns()
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
        rand_col = randint(0, size - 1)
        while not self.legal_columns[rand_col]:
            rand_col = randint(0, size - 1)
        p1_x = randint(0, size - 1)
        p2_x = randint(0, size - 1)
        while not self.can_change[p1_x][rand_col]:
            p1_x = randint(0, size - 1)
        while not self.can_change[p2_x][rand_col]:
            p2_x = randint(0, size - 1)
        self.map[p1_x][rand_col], self.map[p2_x][rand_col] = self.map[p2_x][rand_col], self.map[p1_x][rand_col]
        self.recently_swaped = ((p1_x, rand_col), (p2_x, rand_col))
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

    def assign_legal_columns(self):
        self.legal_columns = np.ones(size, dtype=np.bool_)
        for col_num, column in enumerate(self.can_change.T):
            self.legal_columns[col_num] = any(column)


x = Sudoku()
x.generate_random_solution()
print(x.count_energy())
