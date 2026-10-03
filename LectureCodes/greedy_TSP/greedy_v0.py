import numpy as np
import matplotlib.pyplot as plt

# representation of the problem (TSP)
class Cities:
    def __init__(self, n, seed=None):
        if not (isinstance(n, int) and n > 4):
            raise Exception("n needs to be an integer larger than 4")
        # potentially fix the random realization with the seed
        if seed is not None:
            np.random.seed(seed)
        # store in the object the number of cities
        self.n = n
        # produce the random coordinates for the cities (uniform in [0,1)x[0,1))
        x = np.random.rand(n)
        y = np.random.rand(n)        
        # store the coordinates as attrubutes of the class
        self.x, self.y = x, y
        

def init_config(cities):
    # we need the number of cities
    n = cities.n
    route = np.random.permutation(n)
    return route

# visualization of the problem and configuration
def display(cities, route):
    # need the coordinates of the cities
    x, y = cities.x, cities.y
    # just plot the cities
    plt.clf()
    plt.plot(x, y, "o", color="black")
    
    # plot the route
    # city0 = route[0]
    # city1 = route[1]
    # plt.plot([x[city0], x[city1]], [y[city0], y[city1]], color="red")
    
    # x- coordinates --> creating an array with all the xs in the 
    # the order specified by route
    #[x[city0], x[city1], ...., x[city(n-1)]]
    #[x[route[0]], x[route[1]], ...., x[route[n-1]]]
    #x[route]
    plt.plot(x[route], y[route], color="red")
    
    # add the final edge
    comeback = [route[-1], route[0]]
    plt.plot(x[comeback], y[comeback], color="red")
    




# sketch of the implementation of random-search greedy

def greedy(cities, num_iters, seed=None): # TODO decide arguments
    # potentially fixing the random state to pick the same init configuration
    if seed is not None:
        np.random.seed(seed)
        
    # pick a configuration at random
    x = init_config(cities)
    display(cities, x)
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
