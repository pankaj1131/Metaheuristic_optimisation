"""
Author: Pankaj Singh
file: Novelty_plus.py
"""
import numpy as np
import sys
import random
import time
import logging


class NoveltyPlus:

    def __init__(self, inst_file, max_restart, max_flips, pw, p):
        self.tabu_list = []
        self.instance_file = inst_file
        self.no_of_variables = 0
        self.no_of_clauses = 0
        self.clauses = []
        self.current_configuration = []
        self.max_restarts = max_restart
        self.max_flips = max_flips
        self.net_gain = 0
        self.flip_config = []
        self.unsatisfied_clauses = []
        self.satisfied_clauses = []
        self.no_of_unsatisfied_clauses = 0
        self.no_of_satisfied_clauses = 0
        self.pw = pw
        self.p = p
        self.score = 0

        # uncomment the below code and all the logging code in the file to get logs of the execution

        # logging.basicConfig(filename='log-00-NoveltyPlus_uf20_21_1_exec.txt', level=logging.INFO,
        #                     format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def update_tabu(self, var, age):
        """

        :param var: variable for flip
        :param age: current age of variable --> current iteration
        tabu list updated with dict --> {'var': variable, 'iteration': variable age}
        """
        var_in_tabu_check = np.array([abs(var) == self.tabu_list[i]['var'] for i in range(len(self.tabu_list))])
        occurences = np.where(var_in_tabu_check == True)
        if len(occurences) == 0:
            self.tabu_list.append({'var': abs(var), 'iteration': age})
        else:
            self.tabu_list = list(np.delete(self.tabu_list, occurences))
            self.tabu_list.append({'var': abs(var), 'iteration': age})

    def calc_var_age(self, variable):
        """

        :param variable: variable under consideration
        :return: age of the variable in the tabu list
        """
        var_occurence = np.array([abs(variable) == self.tabu_list[i]['var'] for i in range(len(self.tabu_list))])
        if len(var_occurence) != 0 and True in var_occurence:
            occurence_idx = np.where(var_occurence == True)
            occurence = self.tabu_list[max(occurence_idx)[0]]
            return occurence['iteration']
        else:
            return -1

    def calculate_net_gain(self, config):
        """

        :param config: config to consider for net gain calculation
        :return: net gain using the current config
        """
        net_gain = 0
        self.flip_config = config
        res_of_config_on_clauses = np.apply_along_axis(self.satisfiability_check_with_config, 1, self.clauses)
        pos_of_unsatisfied_clauses = np.where(res_of_config_on_clauses == False)[0]
        unsatisfied_clauses_using_config = self.clauses[pos_of_unsatisfied_clauses]
        net_gain = len(self.unsatisfied_clauses) - len(unsatisfied_clauses_using_config)
        return net_gain

    def split(self, line):
        """
        :param line: line under consideration
        :return: array of words in the line
        """
        return line.split()

    def satisfiability_check_with_config(self, clause):
        """

        :param clause: clause of whose satisfiablity we have to find out
        :return: True or false based on the satisfiablity of the clause
        """
        variable_1 = self.flip_config[abs(clause[0]) - 1] if clause[0] > 0 else not self.flip_config[abs(clause[0]) - 1]
        variable_2 = self.flip_config[abs(clause[1]) - 1] if clause[1] > 0 else not self.flip_config[abs(clause[1]) - 1]
        variable_3 = self.flip_config[abs(clause[2]) - 1] if clause[2] > 0 else not self.flip_config[abs(clause[2]) - 1]
        return variable_1 or variable_2 or variable_3

    def calculate_score(self, config):
        self.flip_config = config
        score = 0
        res_of_config_on_clauses = np.apply_along_axis(self.satisfiability_check_with_config, 1, self.clauses)
        pos_of_unsatisfied_clauses = np.where(res_of_config_on_clauses == False)[0]
        self.unsatisfied_clauses = self.clauses[pos_of_unsatisfied_clauses]
        score = len(pos_of_unsatisfied_clauses)
        pos_of_satisfied_clauses = np.where(res_of_config_on_clauses == True)[0]
        self.satisfied_clauses = self.clauses[pos_of_satisfied_clauses]
        return score

    def noveltyPlus_implementation(self):
        """
        Implementation of the novelty plus algorithm
        """
        for restart in range(self.max_restarts):
            print("Restart number : ", restart + 1)
            # logging.log(logging.INFO, "restart : " + ' INFO --> ' + str(restart + 1))
            self.tabu_list = []
            self.current_configuration = self.generate_rand_truth_values()
            for flip in range(self.max_flips):
                self.score = self.calculate_score(self.current_configuration)
                print("iteration number : ", flip + 1)
                # logging.log(logging.INFO, "iteration number : " + ' INFO --> ' + str(flip + 1))
                if self.score == 0:
                    print('solution found at flip : ', flip + 1)
                    # logging.log(logging.INFO, "solution found at flip : " + ' INFO --> ' + str(flip + 1))
                    print('solution configuration : ', self.current_configuration)
                    # logging.log(logging.INFO, "solution configuration : " + ' INFO --> ' + str(self.current_configuration))
                    return self.current_configuration
                else:
                    print(self.current_configuration)
                    random_unsatisfied_clause_idx = np.random.randint(0, len(self.unsatisfied_clauses))
                    selected_clause = self.unsatisfied_clauses[random_unsatisfied_clause_idx]
                    # logging.log(logging.INFO, "unsatisfied clause selected : " + ' INFO --> ' + str(selected_clause))
                    print("unsatisfied clause selected : ", selected_clause)
                    if random.random() > self.pw:
                        random_idx = np.random.randint(0, len(selected_clause))
                        var_selected_for_flip = selected_clause[random_idx]
                        # logging.log(logging.INFO, "random variable selected for flip : " + ' INFO --> ' + str(var_selected_for_flip))
                        print('random variable selected for flip : ', var_selected_for_flip)
                        self.current_configuration[abs(var_selected_for_flip) - 1] = not self.current_configuration[abs(var_selected_for_flip) - 1]
                        self.update_tabu(var_selected_for_flip, flip + 1)
                    else:
                        config_3_copies = np.array([self.current_configuration, self.current_configuration, self.current_configuration])
                        temp = list(map(lambda x, y: np.put(x, abs(y) - 1, not x[abs(y) - 1]), config_3_copies, selected_clause))
                        net_gain_calc = np.array([self.calculate_net_gain(config_3_copies[i]) for i in range(len(config_3_copies))])
                        ranking_net_gain_arr = np.argsort(np.array(net_gain_calc))
                        var_age_calc = np.array([self.calc_var_age(selected_clause[i]) for i in range(len(selected_clause))])
                        ranking_var_age_arr = np.argsort(var_age_calc)
                        min_age_idx = list(ranking_var_age_arr).index(max(ranking_var_age_arr))
                        max_net_gain_idx = list(ranking_net_gain_arr).index(max(ranking_net_gain_arr))
                        second_best_config = config_3_copies[list(ranking_net_gain_arr).index(1)]
                        second_best_net_gain = net_gain_calc[list(ranking_net_gain_arr).index(1)]
                        second_best_var = selected_clause[list(ranking_net_gain_arr).index(1)]
                        if min_age_idx == max_net_gain_idx:
                            self.current_configuration = config_3_copies[min_age_idx]
                            self.update_tabu(selected_clause[min_age_idx], flip + 1)
                        else:
                            random_probability = random.random()
                            if random_probability > self.p:
                                self.current_configuration = second_best_config
                                self.update_tabu(second_best_var, flip + 1)
                            elif random_probability > 1 - self.p:
                                self.current_configuration = config_3_copies[max_net_gain_idx]
                                self.update_tabu(selected_clause[max_net_gain_idx], flip + 1)
                            print('current best config updated : ', self.current_configuration)
                            # logging.log(logging.INFO, "current best config updated : " + ' INFO --> ' + str(self.current_configuration))

    def lines_preprocessing(self, file):
        """

        :param file: instance file numpy array
        :return: clause numpy array
        """
        comment_lines_indexes = np.core.defchararray.startswith(file, 'c', 0)
        content = file[np.invert(comment_lines_indexes)]
        content = content[np.where(content != '0')]
        content = content[np.where(content != '%')]
        self.no_of_variables = int(content[0].split()[2])
        self.no_of_clauses = int(content[0].split()[3])
        problem_lines = np.core.defchararray.startswith(content, 'p', 0)
        content = content[np.invert(problem_lines)]
        print("number of variables in the instance : ", self.no_of_variables)
        print("number of clauses in the instance : ", self.no_of_clauses)
        # logging.log(logging.INFO, "number of variables in the instance :" + ' INFO --> ' + str(self.no_of_variables))
        # logging.log(logging.INFO, "number of clauses in the instance : " + ' INFO --> ' + str(self.no_of_clauses))
        content = list(content)
        content = [self.split(content[i]) for i in range(len(content))]
        processed_contents = np.array(content).astype(int)[:, :-1]
        return processed_contents

    def generate_rand_truth_values(self):
        binary_assign = np.random.randint(2, size=self.no_of_variables)
        return binary_assign == 1

    def main(self):
        """
        Tasks of this function : 1. Read instance file from the specified instance selected by the user
                                 2. Send the contents of this instance file read for preprocessing, to get the clauses
                                 3. Run the Novelty Plus algorithm once we are done with steps 1 and 2
        """
        inst_file = np.genfromtxt('./Lab-data/Inst/' + self.instance_file, delimiter=',', dtype=None, encoding='utf-8')
        self.clauses = self.lines_preprocessing(inst_file)
        self.noveltyPlus_implementation()


if len(sys.argv) < 1:
    print("Error - Incorrect input")
    print("Expecting python NoveltyPlus.py [instance filename]")
    sys.exit(0)

restarts = 1
flips = 100000
pw = 0.4
p = 0.3
novelty_plus = NoveltyPlus(sys.argv[1], restarts, flips, pw, p)
novelty_plus.main()

