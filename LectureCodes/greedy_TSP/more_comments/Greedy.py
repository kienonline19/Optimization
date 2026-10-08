import numpy as np

## The greedy-random-search generic solver.
## It works on any (discrete) problem, as long as the `probl` object implements
## the right methods:
##
##   init_config()
##   cost()                   [return a cost (float)]
##   propose_move()           [return a move (depends on the problem)]
##   compute_delta_cost(move) [return a delta cost (float)]
##   accept_move(move)
##   copy()                   [return an object like self]
##   display() # optional
##
## Of course, the result may be sub-optimal, there are no guarantees (except
## possibly in the limit of infinite repeats...).
def greedy(probl, repeats = 1, num_iters = 10, seed = None, debug_delta_cost = False):
    ## Optionally set up the random number generator state, for reproducibility
    ## purposes
    if seed is not None:
        np.random.seed(seed)
    ## We repeat the optimization from scratch a number of times.
    ## We need to keep the best cost obtained, and we will save the object
    ## that achieves that cost (to save its internal configuration).
    best_probl = None
    best_c = np.inf
    for step in range(repeats):
        ## Pick an initial config (usually at random)
        probl.init_config()
        # probl.display() # commented out to unclutter the output
        c = probl.cost()
        # print(f"initial cost of run {step} = {c}") # commented out to unclutter the output
        ## This is the core of the algorithm
        last_accepted_t = 0 # useful for inspection (do we have enough num_iters?)
        for t in range(num_iters):
            ## Propose a random move
            move = probl.propose_move()
            ## Does the proposed move improve the cost?
            delta_c = probl.compute_delta_cost(move)
            ## This is a check that the `compute_delta_cost` method gives
            ## results consistent with the cost method. Very computationally
            ## expensive, but useful for debugging.
            ## It works by accepting the move on a copy of the problem,
            ## so the `copy` and `accept_move` methods should work correctly!
            ## (The idea is that those methods are much easier to implement than
            ## `compute_delta_cost`.)
            if debug_delta_cost:
                probl_copy = probl.copy()
                probl_copy.accept_move(move)
                ## Account for floating-point approximations
                assert abs(c + delta_c - probl_copy.cost()) < 1e-10
            if delta_c <= 0:
                ## Accept the move
                probl.accept_move(move)
                c += delta_c # we only need to update the old cost, no need to do it from scratch
                # print(f"t = {t} new_cost = {c}") # commented out to save time
                last_accepted_t = t
        print(f"final cost of run {step} = {c} [obtained at t={last_accepted_t}]")
        ## Save the final config if it was the best so far
        if c < best_c:
            best_c = c
            best_probl = probl.copy()
    # Done. Display and return the best config
    best_probl.display()
    print(f"best cost = {best_c}")
    return best_probl
