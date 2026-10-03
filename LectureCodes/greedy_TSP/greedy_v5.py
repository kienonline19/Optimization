import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


    
class TSP: 
    # storing the instance of the random uniform planar TSP, 
    # and the methods required to represent it and solve it
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
        
        route = np.arange(n) # data type is integer
        self.route = route
        self.init_config() # randomize the current route
        
        
    def __repr__(self):
        s = f"Cities obj with {self.n} cities"
        return s

    def dist(self, city0, city1):
        # should compute the Euclidean distance btw the corresponding points
        # city0/city1 are city identifiers/indices
        x, y = self.x, self.y
        x0, y0 = x[city0], y[city0]
        x1, y1 = x[city1], y[city1]
        d = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)    
    
        return d
    
    def init_config(self):
        n, route = self.n, self.route
        route[:] = np.random.permutation(n)
        
    
    def display(self):
        x, y, n, route = self.x, self.y, self.n, self.route
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
        
    
    def propose_move(self):
        # this doesn't require accessing any property of TSP
        # but it is still defined for this specific problem
        n = self.n
        
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
        
        # create a variable that stores all the information to encode the move
        move = (e1, e2)
        return move
    
    def accept_move(self, move):
        # apply the move directly to the new configuration
        route = self.route
        # decode the move 
        e1, e2 = move
        route[e1+1:e2+1] = route[e2:e1:-1]    
        
    
    def cost(self):
        # sum all distances along the edges of the route
        n, route = self.n, self.route 
        
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
            c += self.dist(city0, city1)
                    
        return c
        
    def delta_cost(self, move):
        c_old = self.cost()
        
        # new_route -> apply a move to the old_route
        # copy the tsp instance -> we now have an indepent copy of the route
        new_tsp = self.copy()
        # apply the move in the instance copy -> old_route -> new_route
        new_tsp.accept_move(move)
        # compute the cost in the instance copy -> cost new_route
        c_new = new_tsp.cost()
        
        delta_c = c_new - c_old

        return delta_c
    
    def copy(self):
        return deepcopy(self)
    


# Implementation of the greedy metaheuristic:
# Can be applied to any problem class that defines the following methods:
# init_config() -> returns a random intial configuration
# cost() -> computes ...
# propose_move()
# display()
# delta_cost(x, y) TODO
# copy() _> returns an indepedent copy of the entire class instance
def greedy(probl, max_iters=10, seed=None, restarts=1):
    if seed is not None:
        np.random.seed(seed)

    best_c = np.inf
    best_probl = None
    for r in range(restarts):
        probl.init_config()
        c = probl.cost() # cost of current configuration
        # display(cities, x) # not necessary
        
        for t in range(max_iters):
            move = probl.propose_move()
            # cnew = cost(cities, y)
            delta_c = probl.delta_cost(move)
            # if cnew <= c:
            if delta_c <= 0:
                # accepting the move
                probl.accept_move(move)
                
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
    
    