import networkx as nx
import numpy as np
from parse import write_input_file


def make_input(s):
    A = np.random.randint(1, high=100 * 1000 - 1, size=(s, s))
    A = A / 1000
    print(A)
    G = nx.from_numpy_matrix(A)
    write_input_file(G, "./part1_inputs/" + str(s) + ".in")


if __name__ == "__main__":
    make_input(30)
    make_input(50)
    make_input(100)
