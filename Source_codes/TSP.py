"""
Author: Pankaj Singh
file: TSP.py
"""
import numpy as np
import sys
# uncomment this to make use of graph utility
# from plot_lib import plot_scatter_graph
import time, copy


class TSP:

    def __init__(self, instance):
        self.instance_file = instance
        self.num_of_nodes = 0
        self.current_tour = []
        self.initial_solution = []
        self.distance = 0
        self.idx = []
        self.edges = []
        self.pertub_repeat_times = 5
        self.traversed_idx = []

    def calc_distance(self, node1, node2):
        """

        :param node1: node1
        :param node2: node2
        :return: euclidean distance between the two nodes
        """
        node1 = node1[1:]
        node2 = node2[1:]
        return np.linalg.norm(node2 - node1)

    def prep_structure_for_dist_calc(self, combinationArr):
        """

        :param combinationArr: current combination of tour under consideration
        :return: total distance of the tour
        """
        distance = 0
        for node1, node2 in zip(combinationArr, combinationArr[1:]):
            distance += self.calc_distance(node1, node2)
        distance += self.calc_distance(combinationArr[-1], combinationArr[0])
        return distance

    def edgesArr(self, curr_tour):
        """

        :param curr_tour: current tour under consideration
        operation : form edges array of the current tour
        """
        self.edges = []
        self.idx = np.arange(1, len(curr_tour) + 1)
        for first, second in zip(self.idx, self.idx[1:]):
            self.edges.append([first, second])
        self.edges.append([self.idx[-1], self.idx[0]])

    def select_random_edge(self):
        """

        :return: random edge selected from the current tours edges array
        """
        random_idx = np.random.randint(0, len(self.edges))
        return self.edges[random_idx], random_idx

    def createInitSolutionAtRandom(self, file_contents):
        """

        :param file_contents: file contents of the instance file selected
        :return: randomly shuffled tour generated
        """
        np.random.shuffle(file_contents)
        return file_contents

    def nearest_neighbour(self, file):
        """

        :param file: file contents of the instance file selected
        :return: nearest neighbour tour
        """
        start_time = time.time()
        random_idx = np.random.randint(0, len(file))
        file = list(file[random_idx: random_idx + 1]) + list(file[0: random_idx]) + list(file[random_idx + 1:])
        for i in range(len(file)):
            if i < len(file) - 1:
                dist_arr = [self.calc_distance(file[i], node2) for node2 in file[i + 1:]]
                min_dist_idx = dist_arr.index(min(dist_arr)) + i + 1 if len(dist_arr) != 0 else i
                file = list(file[0: i + 1]) + list(file[min_dist_idx: min_dist_idx + 1]) + list(file[i + 1: min_dist_idx]) + list(file[min_dist_idx + 1:])
        return np.array(file)

    def createCombinationsandBestSoln(self, first_half, second_half, curr_tour):

        sub_combo_1 = list(self.idx[0:first_half[0]])
        sub_combo_2 = list(self.idx[second_half[0] - 1: first_half[1]])
        sub_combo_2_rev = list(np.flip(np.array(sub_combo_2)))
        sub_combo_3 = list(self.idx[second_half[1] - 1: first_half[2]])
        sub_combo_3_rev = list(np.flip(np.array(sub_combo_3)))
        sub_combo_4 = list(self.idx[second_half[2] - 1:])

        # all combinations possible : -

        combo_1 = curr_tour[np.array(sub_combo_1 + sub_combo_2 + sub_combo_3 + sub_combo_4) - 1]
        combo_2 = curr_tour[np.array(sub_combo_1 + sub_combo_2 + sub_combo_3_rev + sub_combo_4) - 1]
        distance_2 = self.prep_structure_for_dist_calc(combo_2)
        combo_3 = curr_tour[np.array(sub_combo_1 + sub_combo_2_rev + sub_combo_3 + sub_combo_4) - 1]
        distance_3 = self.prep_structure_for_dist_calc(combo_3)
        combo_4 = curr_tour[np.array(sub_combo_1 + sub_combo_2_rev + sub_combo_3_rev + sub_combo_4) - 1]
        distance_4 = self.prep_structure_for_dist_calc(combo_4)
        combo_5 = curr_tour[np.array(sub_combo_1 + sub_combo_3_rev + sub_combo_2 + sub_combo_4) - 1]
        distance_5 = self.prep_structure_for_dist_calc(combo_5)
        combo_6 = curr_tour[np.array(sub_combo_1 + sub_combo_3 + sub_combo_2_rev + sub_combo_4) - 1]
        distance_6 = self.prep_structure_for_dist_calc(combo_6)
        combo_7 = curr_tour[np.array(sub_combo_1 + sub_combo_3_rev + sub_combo_2_rev + sub_combo_4) - 1]
        distance_7 = self.prep_structure_for_dist_calc(combo_7)
        combo_8 = curr_tour[np.array(sub_combo_1 + sub_combo_3 + sub_combo_2 + sub_combo_4) - 1]
        distance_8 = self.prep_structure_for_dist_calc(combo_8)

        # calculate costs :-
        combo_arr = [combo_2, combo_3, combo_4, combo_5, combo_6, combo_7, combo_8]
        distance_arr = [distance_2, distance_3, distance_4, distance_5, distance_6, distance_7, distance_8]
        min_distance = min(distance_arr)
        # print('best minimum distance calculated : ', min_distance)
        return min_distance, combo_arr[distance_arr.index(min_distance)]

    def LocalSearchImplementation(self, curr_tour):
        """

        :param curr_tour: current tour under consideration
        operation :- perform 3-op implementation on the current tour
        :return: tour generated by the 3-opt algorithm
        """
        self.edgesArr(curr_tour)
        self.distance = self.prep_structure_for_dist_calc(curr_tour)
        print('initial distance : ', self.distance)
        edge1, a = self.select_random_edge()
        edge2 = []
        edge3 = []
        """ selection of 1st edge is at random while the other edges are chosen starting from 1st edge till the 
        last edge , every combination"""
        for b in range(len(self.edges)):
            if b != a:
                edge2 = self.edges[b]
                for c in range(b, len(self.edges)):
                    if c != a and c != b:
                        edge3 = self.edges[c]
                        first_half = sorted([edge1[0], edge2[0], edge3[0]])
                        second_half = sorted([edge1[1], edge2[1], edge3[1]])
                        min_distance, min_tour = self.createCombinationsandBestSoln(first_half, second_half, curr_tour)
                        if min_distance < self.distance:
                            curr_tour = min_tour
                            self.distance = min_distance
                            # print(self.current_tour)
        print('Minimum distance thus calculated : ', self.distance)
        return curr_tour
        # print('Tour which generated minimum distance : ', self.current_tour)

        # final state graph
        # tour = np.vstack([self.current_tour, self.current_tour[0]])
        # plot_scatter_graph(tour, self.num_of_nodes, save_title='final_4')

    def pertubationPhase(self, curr_tour):
        """

        :param curr_tour: surrent tour generated by initial 3-opt local search
        operation: perform 2-opt local search implementation
        :return: tour generated
        """
        self.edgesArr(curr_tour)
        for repeat in range(self.pertub_repeat_times):
            random_indexes = np.random.choice(len(self.edges) - 1, 2, replace=False)
            # print("random indexes : ", random_indexes)
            random_edges = np.sort(np.array(self.edges)[random_indexes], axis=0)
            # print("random edges selected : ", random_edges)
            sub_combo_1 = list(self.idx[0: random_edges[0][0]])
            sub_combo_2 = list(np.flip(np.array(list(self.idx[random_edges[0][1] - 1: random_edges[1][0]]))))
            sub_combo_3 = list(self.idx[random_edges[1][1] - 1:])
            combo = curr_tour[np.array(sub_combo_1 + sub_combo_2 + sub_combo_3) - 1]
            curr_tour = combo
        return curr_tour

    def split(self, line):
        """

        :param line: line under consideration
        :return: array of words in the line
        """
        return line.split()

    def lines_preprocessing(self, file):
        """

        :param file: instance file contents
        :return: processed file containing all the cities with their x and y coordinates
        """
        self.num_of_nodes = int(file[0])
        content = file[1:]
        content = [self.split(content[i]) for i in range(len(content))]
        processed_contents = np.array(content).astype(int)
        return processed_contents

    def acceptanceCriterion(self, initial_LS_tour, LS_generated_tour):
        """

        :param initial_LS_tour: the initial tour generated by the LocalSearch implementation: --> 3-opt
        :param LS_generated_tour: The local search tour generated after the pertubation phase
        :return: updated current tour based on the acceptance criteria:- which in this case is 5%
        """
        if np.random.random() > 0.05:
            self.current_tour = LS_generated_tour
        else:
            dist_initial_LS_tour = self.prep_structure_for_dist_calc(initial_LS_tour)
            dist_LS_gen_tour = self.prep_structure_for_dist_calc(LS_generated_tour)
            if dist_LS_gen_tour < dist_initial_LS_tour:
                self.current_tour = LS_generated_tour

    def main(self):
        """
        1. Read the instance file
        2. preprocess the file to get 2D numpy array of the cities from the instance file
        3. create initial solution at random or nearest neighbour
        4. perform 3-opt --> localsearch implementation
        5. repeat
        6. pertubation phase algorithm
        7. Local search implemetation
        8. acceptance criteria
        9. until 5 minutes of time
        """
        inst_file = np.genfromtxt('./Lab-data/Inst/' + self.instance_file, delimiter=',', dtype=None, encoding='utf-8')
        file_contents = self.lines_preprocessing(inst_file)
        # uncomment the below code and comment the self.createInitSolutionAtRandom method line to check result for nearest neighbour

        # self.current_tour = self.nearest_neighbour(file_contents)
        self.current_tour = self.createInitSolutionAtRandom(file_contents)
        # initial state graph ---> uncomment the below code to get the graph of the initial tour
        # initial state graph

        # tour = np.vstack([self.current_tour, self.current_tour[0]])
        # plot_scatter_graph(tour, self.num_of_nodes, save_title='inst_13_tsp_initial_state_random_4')

        self.current_tour = self.LocalSearchImplementation(self.current_tour)
        start_time = time.time()
        while True:
            curr_tour = self.pertubationPhase(self.current_tour)
            LS_generated_tour = self.LocalSearchImplementation(curr_tour)
            self.acceptanceCriterion(self.current_tour, LS_generated_tour)
            if time.time() - start_time > 300:
                break
        print("Best distance calculated : ", self.prep_structure_for_dist_calc(self.current_tour))
        # final state graph ---> uncomment the below code to get the graph of the final tour
        # tour = np.vstack([self.current_tour, self.current_tour[0]])
        # plot_scatter_graph(tour, self.num_of_nodes, save_title='inst_13_tsp_final_state_random_4')


if len(sys.argv) < 1:
    print("Error - Incorrect input")
    print("Expecting python TSP.py [instance filename]")
    sys.exit(0)


tsp = TSP(sys.argv[1])
tsp.main()
