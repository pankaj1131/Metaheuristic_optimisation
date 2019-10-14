"""
Author: Pankaj Singh
file: RTD_distrib.py
"""
import numpy as np
import matplotlib.pyplot as plt
# solution_file_path = './GSAT_tabu_solution_uf20_021.txt'
solution_file_path = './NoveltyPlus_solution_uf20_021.txt'

solution_file = np.genfromtxt(solution_file_path, delimiter=',', dtype=None, encoding='utf-8')


def split(line):
    return line.split()


def pre_process_file(file):
    content = [split(file[i]) for i in range(len(file))]
    processed_contents = np.array(content).astype(float)
    return processed_contents


processed_file = pre_process_file(solution_file)
processed_file[:, :1] = processed_file[:, :1] / 100
plot_file = np.transpose(processed_file)
plt.ylabel('Execution number /100')
plt.xlabel('Time (in seconds)')
plt.plot(sorted(plot_file[1]), plot_file[0])
# plt.show()
# plt.savefig("RTD_GSAT_tabu_100_exec_uf20_21")
plt.savefig("RTD_NoveltyPlus_100_exec_uf20_21")
