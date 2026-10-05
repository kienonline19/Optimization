# script to allow interaction btw problem and solver
import Greedy 
import TSP


tsp = TSP.TSP(100, seed=123376)
best_probl = Greedy.greedy(tsp, max_iters=50000, restarts=5)