import numpy as np

def accept(delta_c, beta):
    if delta_c <= 0: # decreasing cost is good! (as in greedy)
        return True
    # delta_C > 0
    if beta == np.inf: # if beta=inf then we are running greedy, so we reject positive delta_c
        return False
    # return True with the correct probability, else false
    prob = np.exp(-beta * delta_c)
    return np.random.rand() < prob


# implementation of Simulated Annealing
# interface: instance of the problem (class)
# 1 - init_config()
# 2 - display() 
# 3 - cost() 
# 4 - compute_delta_cost(move) (move is an encoding of a move)
# 5 - propose_move() (outputs a encoded move)
# 6 - accept_move(move)  (change the current configuration by applying the move)
# 7 - copy()  (copy and store away the entire object)
def simann(probl, 
           beta0=0.1, beta1=10., annealing_steps=10,
           mcmc_steps=10000, 
           seed=None): 
    # potentially fixing the random state to pick the same init configuration
    if seed is not None:
        np.random.seed(seed)
        
    # define the set of betas in the annealing process
    betas = np.zeros(annealing_steps)
    betas[:-1] = np.linspace(beta0, beta1, annealing_steps-1)
    betas[-1] = np.inf
    
    # pick a configuration at random
    # store the configuration inside of the problem object
    probl.init_config() # O(n) not allocating new memory
    c = probl.cost()
    print(f"initial cost c={c}")
    
    # placeholders for the best cost and configuration
    best_c = c
    best_probl = probl.copy()
    for beta in betas:
        accepted = 0
        for t in range(mcmc_steps):
            # propose a move only encodes the move we want to try
            move = probl.propose_move() # O(1)
            
            delta_c = probl.compute_delta_cost(move) # O(n) bottleneck -> O(1)
            
            # accept the move if it improves the cost
            if accept(delta_c, beta): # we have to accept according to M-H 
                # accept the move
                accepted += 1
                probl.accept_move(move) # O(n)
                c = c + delta_c
                if c < best_c: 
                    # store away the result if it is the current best
                    best_c = c
                    best_probl = probl.copy()
                
        print(f"beta={beta} accept_rate={accepted/mcmc_steps} c={c} best_c={best_c}")
        probl.display() # O(n)
        
    
    print(f"overall best cost c={best_c}")
    best_probl.display()
    
    return best_probl
