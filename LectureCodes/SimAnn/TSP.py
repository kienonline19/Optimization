import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# representation of the problem (TSP)
class TSP:
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
        
        # store also the route inside the object
        self.route = np.zeros(n, dtype=int)
        self.init_config()
        
        # store all the distances once and for all in a matrix
        # dist = np.zeros((n,n))
        # for city1 in range(n):
        #     for city2 in range(city1+1, n):
        #         x1, y1 = x[city1], y[city1]
        #         x2, y2 = x[city2], y[city2]
        #         d = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        #         dist[city1, city2] = d
        #         dist[city2, city1] = d
        # self.dist = dist
        
        xT = x.reshape((n, 1))
        yT = y.reshape((n, 1))
        self.dist = np.sqrt((xT - x)**2 + (yT - y)**2)

    # def dist(self, city1, city2):
    #     x1, y1 = self.x[city1], self.y[city1]
    #     x2, y2 = self.x[city2], self.y[city2]
    #     d = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    #     return d

    def init_config(self):
        # we need the number of cities
        n = self.n
        # change the route in-place
        self.route[:] = np.random.permutation(n)
        
    # visualization of the problem and configuration
    def display(self):
        # need the coordinates of the cities
        n, x, y, route = self.n, self.x, self.y, self.route
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
        # plt.plot(x[route], y[route], color="red")
        
        # add the final edge
        # comeback = [route[-1], route[0]]
        # plt.plot(x[comeback], y[comeback], color="red")
        
        # TASK
        # use modulus (remainder) operation to plot the path with a single line
        plt.plot(x[route[np.arange(n+1)%n]], y[route[np.arange(n+1)%n]], color="red")
        plt.pause(0.0001)
    
    def propose_move(self): # O(1)
        # get how many cities are there
        n = self.n
        
    
        # TODO: fix this for problems with the edge extrection
        # Special cases to avoid 
        # 1) same edge
        # 2) e1 > e2
        # 3) e1 + 1 = e2
    
        # pick two edges at random
        # e1 = np.random.randint(n)
        # e2 = np.random.randint(n)
        
        # while "conditions not met":
        #     e1 = np.random.randint(n)
        #     e2 = np.random.randint(n)
        
        # while True:
        #     e1 = np.random.randint(n)
        #     e2 = np.random.randint(n)
        #     if e1 > e2:
        #         # potentially reorder e1 and e2
        #         e1, e2 = e2, e1
        #     if e1 != e2 and e1+1 != e2 and (e2+1) % n != e1:
        #         break
            
        # TASK: this can be done without rejections
        # hint: use the modulus operation
        # without np.choice
        e1 = np.random.randint(n)
        e2 = (e1 + 2 + np.random.randint(n-3)) % n
        if e1 > e2: e1, e2 = e2, e1
            
        # print(f"e1={e1} e2={e2}")
        
        move = (e1, e2) # encoding / packing the move
        
        return move
        
    def accept_move(self, move):
        # changing in-place the route store in the problem object
        e1, e2 = move # deconding / unpacking the move
        route = self.route
        # invert the order of the route between e1+1 and e2
        # route[e1+1:e2+1] = (route[e1+1:e2+1])[::-1]
        route[e1+1:e2+1] = route[e2:e1:-1]
    
    
    def cost(self):
        # cumulative distance along the route
        n, route = self.n, self.route
        # c = 0.
        # for i in range(n-1):
        #     city1 = route[i]
        #     city2 = route[i+1]
        #     c += dist(cities, city1, city2) # TODO
        # # adding the comeback cost (as in the display function)
        # city1 = route[-1]
        # city2 = route[0]
        # c += dist(cities, city1, city2)
        
        c = 0.
        for i in range(n):
            city1 = route[i]
            city2 = route[(i+1) % n]
            c += self.dist[city1, city2]
        
        return c
    
    def compute_delta_cost(self, move): # O(n)
        # naive (but safe) implementation
        # old_cost = self.cost() # O(n)
        # # copying the entire problem object and applying the move only in the
        # # copy
        # # new_probl = self.copy()
        # # new_probl.accept_move(move)
        # # new_cost = new_probl.cost()
        
        # self.accept_move(move) # we temporarely change the current config
        # new_cost = self.cost()
        # self.accept_move(move) # we swap back the edges
        
        # delta_c_naive = new_cost - old_cost
        
        # implement an efficient version of this function O(1)
        # there are only 4 edges involved in the computation!
        e1, e2 = move # deconding / unpacking the move
        n, route = self.n, self.route
        city11, city12 = route[e1], route[(e1+1) % n]
        city21, city22 = route[e2], route[(e2+1) % n]
        old_edges_cost = self.dist[city11, city12] + self.dist[city21, city22] # add up the old links 
        new_edges_cost = self.dist[city11, city21] + self.dist[city12, city22] # fix this
        
        delta_c = new_edges_cost - old_edges_cost
        
        # check for consistency with the naive version
        # assert abs(delta_c - delta_c_naive) < 1e-10 

        return delta_c
    
    def copy(self):
        # this could be optimized (specialized for the problem)
        return deepcopy(self)

