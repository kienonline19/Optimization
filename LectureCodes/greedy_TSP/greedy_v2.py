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
    plt.pause(0.01)
    

def propose_move(route):
    n = len(route)
    
    
    # checks that the choice "makes sense"
    # e1 = e2 = 0
    # while e1 == e2:
    #     e1 = np.random.randint(n) # random integer
    #     e2 = np.random.randint(n) # random integer
    
    # edges chosen uniformly at random with constraints
    while True:
        e1 = np.random.randint(n) # random integer
        e2 = np.random.randint(n) # random integer
        if e1 > e2:
            # swap them
            e1, e2 = e2, e1
        if e1 != e2 and e1+1 != e2 and not (e1 == 0 and e2 == n-1): # cover the case where we pick first and last edges
            #conditions are met
            break
        
    # print(f"e1={e1} e2={e2}")
    
    # route[e1+1:e2+1] = route[e1+1:e2+1][::-1]
    new_route = route.copy()
    new_route[e1+1:e2+1] = new_route[e2:e1:-1]    
    
    # we expect new_route to be different from route
    # assert not np.array_equal(route, new_route)
    
    return new_route

def dist(cities, city0, city1):
    # should compute the Euclidean distance btw the corresponding points
    # city0/city1 are city identifiers/indices
    x, y = cities.x, cities.y
    x0, y0 = x[city0], y[city0]
    x1, y1 = x[city1], y[city1]
    d = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)    

    return d

def cost(cities, route):
    # sum all distances along the edges of the route
    n = cities.n 
    
    # c = 0.0
    # for e in range(n-1):
    #     # cosmetics for readability
    #     city0 = route[e]
    #     city1 = route[e+1]
    #     # actual operation
    #     c += dist(cities, city0, city1)
        
    # city0 = route[-1]
    # city1 = route[0]
    # # actual operation
    # c += dist(cities, city0, city1)
    
    c = 0.0
    for e in range(n):
        # cosmetics for readability
        city0 = route[e]
        city1 = route[(e+1) % n]
        # actual operation
        c += dist(cities, city0, city1)
                
    return c
    
    

def greedy(cities, max_iters=10, seed=None, restarts=1):
    if seed is not None:
        np.random.seed(seed)

    best_c = np.inf
    best_x = None
    for r in range(restarts):
        x = init_config(cities)
        c = cost(cities, x) # cost of current configuration
        # display(cities, x) # not necessary
        
        for t in range(max_iters):
            y = propose_move(x)
            cnew = cost(cities, y)
            if cnew <= c:
                # accepting the move
                x = y
                c = cnew
                # display(cities, x)
                print(f"t={t} c={c}")
                
        print(f"final cost c={c}")
        display(cities, x)
        if c < best_c:
            best_c = c
            best_x = x
            
    print(f"best cost c={best_c}")
        
    return x
    
    