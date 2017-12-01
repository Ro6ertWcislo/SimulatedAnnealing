from bitmap import BitMap
from energy import *
from matplotlib import pyplot as plt
from anneal import solve_random, solve_neighbour
from salesman import Path

# bitmap example
x = BitMap()
x.set_energy_and_neighbourhood(mandelbrot_energy, mandelbrot_neighbours)
x.generate_with_density(110, 0.3)
x.dot_size = 30
x.draw()
solve_random(x, np.logspace(3, -2, 100000))
x.draw()
plt.plot(range(len(x.energy)), x.energy)
plt.show()
#######################################
x = BitMap()
x.set_energy_and_neighbourhood(weird_energy,eight_friends_neighbours)
x.generate_with_density(110, 0.3)
x.dot_size = 30
x.draw()
solve_random(x, np.logspace(3, -2, 100000))
x.draw()


# salesman example

x = Path()
x.generate_clusters(2, 15)
solve_random(x, np.logspace(4, -1, 100000))
x.draw()

x.generate_uniform(20,100)
solve_random(x, np.logspace(4, -1, 10000))
x.draw()
