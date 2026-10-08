from TSP import TSP
from SimAnn import simann 


tsp = TSP(200, seed=45871231)

best_probl = simann(tsp, 
                    beta0=2., beta1=100., annealing_steps=50,
                    mcmc_steps=10000, seed=12812323)