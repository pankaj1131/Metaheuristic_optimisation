# Metaheuristic_optimisation

This project demonstrates the implementation of the following algorithms used for solving Boolean Satisfiability problems(SAT) and Travelling salesman problems(TSP):

1. GSAT with Tabu list
2. Novelty Plus
3. TSP problem solved using Local search with pertubation phase.

## Installation guideline:

Install the packages listed in the requirements.txt file(for pip users) :

```
pip install -r requirements.txt
```

## Running the code:

```
python python_filename.py instance_name
```

There are three options for python_filename which will be one of the 3 algorithms:
1. GSAT_tabu_list.py
2. Novelty_plus.py 
3. TSP.py  

If you select Boolean Satisfiability Problem solving i.e. options 1 or 2, you will have two instance_name options which can be found under the directory source_codes/Lab-data:
i) uf20-020.cnf
ii) uf20-021.cnf

If you select the TSP problem solved using Local search with pertubation phase option , you will have two instance_name options available:
i) inst-0.tsp
ii) inst-13.tsp

Now you are all set to run the code.

## Graphical Results:

The graphical results of running the three algorithms can be found inside the Graphs folder:
It has two sub-folders:
1. RTD (Real-time distribution graphs for 1st and second algorithm)
2. TSP (Containing graphs of two different configurations for TSP problems for setting the intitial configuration)
   i) Nearest_neighbour
   ii) Random_initial_solution
   The mode can be set inside the code for TSP itself.
   
## Author:
Pankaj Singh (MSc. Artificial Intelligence)

