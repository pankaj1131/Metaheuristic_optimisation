"""
Author: Pankaj Singh
file: GSAT_graph_util.py
"""
import matplotlib.pyplot as plt


def plot_graph(x, y):
    # fitness = [22189513, 21910572, 21881666, 21847409]
    # plt.suptitle(sub_title)
    plt.xlabel('Flip')
    plt.ylabel('Score')
    plt.plot(x, y)
    plt.show()
    # plt.savefig('config_5_3_1_8')


# plot_graph([0, 1, 2, 3], [3, 2, 9, 18])
