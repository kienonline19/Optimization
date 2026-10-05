import numpy as np


# Implementation of the greedy metaheuristic:
# Can be applied to any problem class that defines the following methods:
# init_config() -> returns a random intial configuration
# cost() -> computes ...
# propose_move()
# display()
# delta_cost()
# copy() _> returns an indepedent copy of the entire class instance
def greedy(probl, max_iters=10, seed=None, restarts=1):
    if seed is not None:
        np.random.seed(seed)

    best_c = np.inf
    best_probl = None
    for r in range(restarts):
        probl.init_config() # O(n)
        c = probl.cost() # O(n) cost of current configuration
        # display(cities, x) # not necessary
        
        for t in range(max_iters):
            move = probl.propose_move() # O(1)
            # cnew = cost(cities, y)
            delta_c = probl.delta_cost(move) # O(n) -> O(1)
            # if cnew <= c:
            if delta_c <= 0:
                # accepting the move
                probl.accept_move(move) # O(n)
                
                c += delta_c
                # display(cities, x)
                print(f"t={t} c={c}")
                
        print(f"final cost c={c}")
        probl.display()
        if c < best_c:
            best_c = c
            best_probl = probl.copy()
            
    print(f"best cost c={best_c}")
    best_probl.display()
        
    return best_probl
    
    