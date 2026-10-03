import numpy as np
import matplotlib.pyplot as plt


    
class Cities: # storing the instance of the random uniform planar TSP
    def __init__(self, n, seed=None):
        # check that n is an integer and larger equal than 4
        if not (isinstance(n, int) and n >= 4):
            raise Exception("you should provide an integer larget equal than 4")
        self.n = n
        
        if seed is not None:
            np.random.seed(seed)
        
        x = np.random.rand(n)
        y = np.random.rand(n)
        self.x, self.y = x, y
        
    def __repr__(self):
        s = f"Cities obj with {self.n} cities"
        return s

def init_config(cities):
    n = cities.n
    route = np.random.permutation(n)
    return route

def display(cities, route):
    x, y, n = cities.x, cities.y, cities.n
    plt.clf()
    # plotting the cities positions
    plt.plot(x, y, '.', color="black")
    
    # plotting the route
    # first edge
    # for i in range(n-1):
    #     city0 = route[i] # time index in the route
    #     city1 = route[i+1]
    #     plt.plot([x[city0], x[city1]], [y[city0], y[city1]], color="red")
    
    plt.plot(x[route], y[route], color="red")

    # comeback to the initial city
    city0 = route[-1] 
    city1 = route[0]
    plt.plot([x[city0], x[city1]], [y[city0], y[city1]], color="red")

    # TASK: there is a way to avoid hard-coding the last edge
    # indexing trick plus a modulus operation
    

def propose_move(route):
    n = len(route)
    e1 = np.random.randint(n) # random integer
    e2 = np.random.randint(n) # random integer
    
    # checks that the choice "makes sense"
    
    # route[e1+1:e2+1] = route[e1+1:e2+1][::-1]
    new_route = route.copy()
    new_route[e1+1:e2+1] = new_route[e2:e1:-1]    
    return new_route
    
    

def greedy(cities, max_iters=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
        
    x = init_config(cities)
    for t in range(max_iters):
        y = propose_move(x)
        if cost(y) <= cost(x):
            # accepting the move
            x = y