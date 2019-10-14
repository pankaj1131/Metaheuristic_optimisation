"""
Author: Pankaj Singh
file: plot_lib.py
"""
import matplotlib.pyplot as plt
import numpy as np


def plot_scatter_graph(positions, N, save_title):

    fig, ax = plt.subplots(1, sharex=True, sharey=True)         # Prepare 2 plots
    ax.set_title('Raw nodes')
    ax.scatter(positions[:, 1:2], positions[:, -1])             # plot A
    for node1, node2 in zip(positions, positions[1:]):
        ax.annotate("",
                       xy=node1[1:], xycoords='data',
                       xytext=node2[1:], textcoords='data',
                       arrowprops=dict(arrowstyle="-",
                                       connectionstyle="arc3"))

        # plt.plot(node1[1:], node2[1:], 'o-')
    # plt.show()
    plt.savefig(save_title)


# a = np.array([[1, 823170, 415922], [2, 793699, 274913], [3, 981665, 218777], [4, 878910, 431320], [1, 823170, 415922]])
# plot_scatter_graph(a, 4)
