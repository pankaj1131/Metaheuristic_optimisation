"""
Author: Pankaj Singh
file: GSAT_tabu_list.py
"""
import numpy as np
import sys
import time
# from GSAT_graph_util import plot_graph
import logging


class GSAT_Tabu:

    def __init__(self, inst_file, tabu_list_size, max_restart, max_flips):
        self.tabu_size = tabu_list_size
        self.tabu_list = []
        self.instance_file = inst_file
        self.no_of_variables = 0
        self.no_of_clauses = 0
        self.clauses = []
        self.current_configuration = []
        self.max_restarts = max_restart
        self.max_flips = max_flips
        self.score = 0
        self.flip_config = []
        self.unsatisfied_clauses = []
        self.scoring_distrib_arr = []
        self.itr_where_flipped_arr = []
        # uncomment the below code and all the logging code in the file to get logs of the execution

        # logging.basicConfig(filename='log-00-GSAT_Tabu_list_uf20_21_1_exec.txt', level=logging.INFO,
        #                     format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def split(self, line):
        """

        :param line: line under consideration
        :return: array of words in the line
        """
        return line.split()

    def satisfiability_check(self, clause):
        """

        :param clause: clause of whose satisfiablity we have to find out
        :return: True or false based on the satisfiablity of the clause
        """
        variable_1 = self.current_configuration[abs(clause[0]) - 1] if clause[0] > 0 else not self.current_configuration[abs(clause[0]) - 1]
        variable_2 = self.current_configuration[abs(clause[1]) - 1] if clause[1] > 0 else not self.current_configuration[abs(clause[1]) - 1]
        variable_3 = self.current_configuration[abs(clause[2]) - 1] if clause[2] > 0 else not self.current_configuration[abs(clause[2]) - 1]
        return variable_1 or variable_2 or variable_3

    def calc_score(self):
        """

        :return: calculated score without using the configuration but instead with the clobal current configuartion
        """
        self.score = 0
        res_of_config_on_clauses = np.apply_along_axis(self.satisfiability_check, 1, self.clauses)
        pos_of_unsatisfied_clauses = np.where(res_of_config_on_clauses == False)[0]
        self.unsatisfied_clauses = self.clauses[pos_of_unsatisfied_clauses]
        self.score = len(pos_of_unsatisfied_clauses)
        return self.score

    def satisfiability_check_with_config(self, clause):
        """

        :param clause: clause under consideration
        :return: satisfiability of the clause
        """
        variable_1 = self.flip_config[abs(clause[0]) - 1] if clause[0] > 0 else not self.flip_config[abs(clause[0]) - 1]
        variable_2 = self.flip_config[abs(clause[1]) - 1] if clause[1] > 0 else not self.flip_config[abs(clause[1]) - 1]
        variable_3 = self.flip_config[abs(clause[2]) - 1] if clause[2] > 0 else not self.flip_config[abs(clause[2]) - 1]
        return variable_1 or variable_2 or variable_3

    def calc_score_using_config(self, config):
        """

        :param config: configuration to keep in mind while calculating the satisfiability of clauses
        :return: number of unsatisfied clauses ==> score
        """
        self.flip_config = config
        res_of_config_on_clauses = np.apply_along_axis(self.satisfiability_check_with_config, 1, self.clauses)
        pos_of_unsatisfied_clauses = np.where(res_of_config_on_clauses == False)[0]
        score = len(pos_of_unsatisfied_clauses)
        return score

    def check_tabu_list(self, variable):
        """

        :param variable: variables in the clause
        :return: False :- if its in the tabu list
                 True :- if its not in the tabu list
        """
        return abs(variable) not in self.tabu_list

    def GSAT_implementation(self):
        """ GSAT algorithm implementation """
        for attempt in range(self.max_restarts):
            print('restart : ', attempt + 1)
            # logging.log(logging.INFO, "restart : " + ' INFO --> ' + str(attempt + 1))
            self.tabu_list = []
            self.current_configuration = self.generate_rand_truth_values()
            print('initial config = ', self.current_configuration)
            # logging.log(logging.INFO, "initial config : " + ' INFO --> ' + str(self.current_configuration))
            for flip in range(self.max_flips):
                print('flip : ', flip + 1)
                # logging.log(logging.INFO, "flip : " + ' INFO --> ' + str(flip + 1))
                # calculate score at each flip
                self.score = self.calc_score()
                # if the score is = 0 then stop the whole process as a solution is found
                if self.score == 0:
                    # logging.log(logging.INFO, "Solution found at restart : " + ' INFO --> ' + str(attempt + 1) + " flip : " + str(flip + 1))
                    print('Solution found at restart : ', attempt + 1, ' flip number : ', flip + 1)
                    # logging.log(logging.INFO, "solution configuration : " + ' INFO --> ' + str(self.current_configuration))
                    print('solution configuration : ', self.current_configuration)
                    return self.current_configuration
                else:
                    # make 3 copies of the current configuration
                    copy_3_config = np.array([self.current_configuration, self.current_configuration, self.current_configuration])
                    # select a random clause from the list of unsatisfied clauses
                    selected_random_clause_idx = np.random.randint(0, len(self.unsatisfied_clauses))
                    clause_for_flip = self.unsatisfied_clauses[selected_random_clause_idx]

                    # check tabu if the variables in this clause are present in tabu or not,
                    # based on that it will return False if the variable is in tabu list and True if its not in
                    # the tabu list
                    tabu_check_result = np.apply_along_axis(self.check_tabu_list, 0, [clause_for_flip])

                    # selecting only those variables in a clause that are not in the tabu list
                    clause_for_flip = clause_for_flip[tabu_check_result]
                    # reduce the 3 copies of current configuration to the same amount as that of the number of variables
                    #  in the clause that are not in tabu list
                    copy_3_config = copy_3_config[tabu_check_result]

                    # Just a check if there exists any variable in the clause that is not in the tabu list
                    if len(clause_for_flip) != 0:
                        # perform flips of variables in the clause simultaneously on each of the copies of
                        # current cofiguration
                        temp = list(map(lambda x, y: np.put(x, abs(y) - 1, not x[abs(y) - 1]), copy_3_config, clause_for_flip))

                        # calculate scores of each configuration
                        scores_of_flipping = [self.calc_score_using_config(copy_3_config[i]) for i in range(len(copy_3_config))]

                        # select the variable which when flipped resulted in the minimum score
                        var_selected_for_flip = clause_for_flip[scores_of_flipping.index(min(scores_of_flipping))]
                        # logging.log(logging.INFO, "minimum score after flipping : " + ' INFO --> ' + str(min(scores_of_flipping)))
                        print('minimum score after flipping : ', min(scores_of_flipping))
                        # logging.log(logging.INFO, "tabu list before variable flipped : " + ' INFO --> ' + str(self.tabu_list))
                        print('tabu list before variable flipped : ', self.tabu_list)

                        # check if current score is better than the min score calculated above
                        if min(scores_of_flipping) < self.score and abs(var_selected_for_flip) not in self.tabu_list:
                            # logging.log(logging.INFO, "variable selected for flip : " + ' INFO --> ' + str(var_selected_for_flip))
                            print('variable selected for flip : ', var_selected_for_flip)
                            self.score = min(scores_of_flipping)
                            # update tabu list
                            if len(self.tabu_list) < self.tabu_size:
                                self.tabu_list.append(abs(var_selected_for_flip))
                                print('tabu list after variable flipped : ', self.tabu_list)
                                # logging.log(logging.INFO,
                                #             "tabu list after variable flipped : " + ' INFO --> ' + str(self.tabu_list))
                            else:
                                del self.tabu_list[0]
                                self.tabu_list.append(abs(var_selected_for_flip))
                                # logging.log(logging.INFO,
                                #             "tabu list after variable flipped : " + ' INFO --> ' + str(self.tabu_list))
                                print('tabu list after variable flipped : ', self.tabu_list)
                            # update the current configuration
                            self.current_configuration = copy_3_config[scores_of_flipping.index(min(scores_of_flipping))]
                # logging.log(logging.INFO,
                #             "config selected : " + ' INFO --> ' + str(self.current_configuration))
                print('config selected : ', self.current_configuration)

    def lines_preprocessing(self, file):
        """

        :param file: instance file contents, which was earlier read
        :return: Numpy array containing all the clauses in the instance file
        """
        # remove all lines with starting character as c --> comment lines
        comment_lines_indexes = np.core.defchararray.startswith(file, 'c', 0)
        content = file[np.invert(comment_lines_indexes)]
        # remove all lines where '0' or '%' for keeping just the clauses in the file
        content = content[np.where(content != '0')]
        content = content[np.where(content != '%')]
        # the first line starting with p contains info like --> number of variables in the clauses and number of clauses
        # in the file
        self.no_of_variables = int(content[0].split()[2])
        self.no_of_clauses = int(content[0].split()[3])
        # logging.log(logging.INFO, "number of variables in the instance :" + ' INFO --> ' + str(self.no_of_variables))
        print("number of variables in the instance : ", self.no_of_variables)
        print("number of clauses in the instance : ", self.no_of_clauses)
        # logging.log(logging.INFO, "number of clauses in the instance : " + ' INFO --> ' + str(self.no_of_clauses))
        # remove problem lines ---> the ones starting with p
        problem_lines = np.core.defchararray.startswith(content, 'p', 0)
        content = content[np.invert(problem_lines)]
        content = list(content)
        # split contents to form a 2D array
        content = [self.split(content[i]) for i in range(len(content))]
        # Take only the first three columns of each clause, as the 4th variable is a 0, and we must not include that
        # also convert the type of the array to integer
        processed_contents = np.array(content).astype(int)[:, :-1]
        return processed_contents

    def generate_rand_truth_values(self):
        binary_assign = np.random.randint(2, size=self.no_of_variables)
        return binary_assign == 1

    def main(self):
        """
        Tasks of this function : 1. Read instance file from the specified instance selected by the user
                                 2. Send the contents of this instance file read for preprocessing, to get the clauses
                                 3. Run the GSAT algorithm once we are done with steps 1 and 2
        """
        inst_file = np.genfromtxt('./Lab-data/Inst/' + self.instance_file, delimiter=',', dtype=None, encoding='utf-8')
        self.clauses = self.lines_preprocessing(inst_file)
        self.GSAT_implementation()


if len(sys.argv) < 1:
    print("Error - Incorrect input")
    print("Expecting python GSAT_Tabu.py [instance filename]")
    sys.exit(0)

restarts = 10
flips = 1000
tabu_size = 5
gsat_tabu = GSAT_Tabu(sys.argv[1], tabu_size, restarts, flips)
gsat_tabu.main()

