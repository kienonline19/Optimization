# sketch of the implementation of random-search greedy

def greedy(..., num_iters): # TODO decide arguments
    # pick a configuration at random
    x = init_config() # TODO put arguments 
    # main loop of Greedy
    for t in range(num_iters):
        # propose a move 
        y = propose_move(x) # TODO
        # accept the move if it improves the cost
        if cost(y) <= cost(x): # TODO implement cost
            # accept the move
            x = y # update your configuration
        # else:
        #     pass
        #     x = x 
    return x
