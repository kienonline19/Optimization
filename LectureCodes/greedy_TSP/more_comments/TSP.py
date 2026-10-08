import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy

class TSP:
    def __init__(self, n, seed = None):
        if not (isinstance(n, int) and n >= 4):
            raise Exception("n must be an int greater than 3")
        self.n = n

        ## Set up the random number generator to some arbitrary but
        ## specific configuration, so that the next two calls
        ## will always produce the same result. This helps a lot
        ## with debugging.
        if seed is not None:
            np.random.seed(seed)

        ## Extract n random coordinates uniformly in the [0,1)x[0,1) square
        x = np.random.rand(n)
        y = np.random.rand(n)
        ## Store them as attributes inside the object
        self.x, self.y = x, y
        ## The fact that we have both x and self.x is just convenient for the
        ## code below, to make it shorter. But beware: it may get confusing if
        ## you do things like x=something because that wouldn't affect self.x!


        ## Pre-compute the distances. Since they don't change, we can do this
        ## once in the constructor and use the results in the rest of the code.
        ## We store the distance between any two points in a symmetric nxn
        ## matrix. The diagonal elements will be zero.

        ## version 0: double-for loop (rather slow)
        ## Since the matrix is symmetric, we just need to compute the upper
        ## triangle of the matrix, excluding the diagonal; the lower triangle
        ## is copied over. So the index `city2` will start from `city1+1`, and
        ## we fill two slots of the matrix at a time.

        # dist = np.zeros((n, n))
        # for city1 in range(n):
        #     for city2 in range(city1 + 1, n):
        #         x1, y1 = x[city1], y[city1]
        #         x2, y2 = x[city2], y[city2]
        #         d = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        #         dist[city1,city2] = d
        #         dist[city2,city1] = d

        ## version 1: exploiting numpy broadcasting rules
        ##            (shorter and much faster)
        ##   The key insight here is that if we have a row vector x and we
        ##   subtract the same vector transposed, we obtain an n x n matrix
        ##   whose elements are aᵢⱼ = (xᵢ - xⱼ), i.e. a matrix of pairwise
        ##   differences.
        ##   Then we square it (each element gets squared); we do the same for
        ##   y; we sum the two results and take the sqrt of that (np.sqrt is
        ##   applied element-wise). The final result is a matrix d whose
        ##   elements are
        ##     dᵢⱼ = √((xᵢ - xⱼ)² + (yᵢ - yⱼ)²)
        ##   which is exactly what we want
        ##   We need some "transposed" versions of x and y (as column matrices)
        xT = x.reshape((n,1))
        yT = y.reshape((n,1))
        ## Compute the whole distance matrix in one line!
        dist = np.sqrt((x - xT)**2 + (y - yT)**2)

        ## Store it in the object
        self.dist = dist

        self.route = np.zeros(n, dtype=int)
        self.init_config()

    ## Initialize (or reset) the current configuration
    def init_config(self):
        ## Create local variables to reflect the class attributes
        n = self.n
        ## We just set the configuration to a random permutation of the
        ## indices. Luckily, numpy.random has a function for that.
        self.route[:] = np.random.permutation(n)


    ## Plot the cities and the current configuration
    def display(self):
        ## Create local variables to reflect the class attributes
        x, y = self.x, self.y
        route = self.route
        ## Clear the figure
        plt.clf()
        ## Plot the cities as circles
        plt.plot(x, y, 'o')

        ## Plot the route. We need to permute the points according to the route.
        ## Indeed, given the route, the traversed cities are:
        ##     city0 = route[0]
        ##     city1 = route[1]
        ##     ...
        ## and then we would plot something like this:
        ##     plt.plot([x[city0], x[city1], ...], [y[city0], y[city1], ...])
        ## so we need a way to write this (and the analogous for y):
        ##     x[route[0]], x[route[1]], x[route[2]], ..., x[route[n-1]]
        ## luckily the syntax for that is very easy:
        ##     x[route]
        ## In conclusion (here the '-' explicitly asks to use lines, and we also
        ## set the color):
        plt.plot(x[route], y[route], '-', c='orange')

        ## The previous plot misses the link between the last and the first
        ## cities in the route, which is implicit in our representation. We add
        ## it explicitly, matching the style of the previous plot.
        xcomeback = [x[route[-1]], x[route[0]]]
        ycomeback = [y[route[-1]], y[route[0]]]

        plt.plot(xcomeback, ycomeback, '-', c='orange')

        ## Pause to actually see something (otherwise wouldn't even update the
        ## display until the end)
        plt.pause(0.00001)

    ## What is the cost of the current configuration?
    ## (computed from scratch, thus O(n))
    def cost(self):
        ## Create local variables that reflect the class' attributes,
        ## purely to make the rest of the code shorter
        n, route, dist = self.n, self.route, self.dist
        c = 0.0
        for e in range(n):
            ## The edge number `e` connects the e-th city in the route and the
            ## (e+1)-th city in the route. Except the last edge, which connects
            ## the (n-1)-th edge with the 0-th edge. In order to deal with that
            ## special case, we use (e+1)%n which makes the indices "cycle
            ## around". For e<n-1 the modulus operator has no effect, for
            ## e==n-1 then (e+1)%n=n%n=0 which is what we want.
            city1 = route[e]
            city2 = route[(e+1) % n]
            c += dist[city1, city2]
        return c

    ## Propose a valid random move. We want to propose the "cross two random
    ## links" type of move. We encode a move with just two indices, in a tuple,
    ## each of them representing an edge index along the route. As before, the
    ## e-th edge connects the e-th city in the route and the (e+1)-th city in
    ## the route.
    ## The choice e1,e2 will mean: swap the links (e1,e1+1) and (e2,e2+1)
    ## so that in the end we get a link (e1,e2) and a link (e1+1,e2+1).
    def propose_move(self):
        n = self.n
        ## Since not all moves are valid, we start a loop. We want to keep
        ## producing random moves until we get to a valid one
        while True:
            ## Extract two random edge indices
            e1 = np.random.randint(n) # edge between route[e1], route[e1+1]
            e2 = np.random.randint(n) # edge between route[e2], route[e2+1]
            ## For reasons of simplicity, we sort them such that e1 <= e2.
            ## We can do this because the probabilities are uniform for
            ## both `e1` and `e2`.
            if e1 > e2:
                e1, e2 = e2, e1
            ## If the move is valid, we want to get out of the loop.
            ## The move is valid if it produces a configuration which is
            ## different from the current one.
            ## There are two basic conditions when that may happen:
            ## 1) the two links are the same (meaning `e1 == e2`)
            ## 2) the two links are adjacent (meaning that `e1` and `e2` differ
            ##    by one)
            ## The second condition has a special case at the end of
            ## the route.
            if e1 != e2 and e1 + 1 != e2 and not (e1 == 0 and e2 == n-1):
                break

        ## If we're here, we have found a valid move.
        ## Pack it up in a tuple and return it.
        move = (e1, e2)
        return move

    def accept_move(self, move):
        ## Unpack the move
        e1, e2 = move
        ## Extract a reference to the route from the object
        ## IMPORTANT: this works fine because we are going to modify
        ##            the *contents* of `route` in-place, and `route`
        ##            and `self.route` share the same data. Keep in
        ##            mind however that they are *not* the same variable.
        route = self.route
        ## The effect of accepting the "cross two links" move is to
        ## reverse the route indices between `e1+1` (included) and
        ## `e2+1` (excluded, i.e. up to `e2`). So we need to overwrite
        ## that route range with its own contents reversed.
        ## On the right-hand-side, the `-1` is the step and it means
        ## "go in reverse". Because we go in the reverse direction,
        ## the range starts from `e2` (included) and ends at `e1`
        ## (excluded, i.e. it actually stops at `e1+1`)
        route[e1+1:e2+1] = route[e2:e1:-1]

    ## What would be the change in the cost if we were to accept the proposed
    ## move?
    def compute_delta_cost(self, move):
        ## Unpack the move
        e1, e2 = move
        ## Create local variables that reflect the class' attributes,
        ## purely to make the rest of the code shorter
        n, route, dist = self.n, self.route, self.dist
        ## Cities involved in the first (old) edge (cf. with the cost method)
        city11, city12 = route[e1], route[(e1+1) % n]
        ## Cities involved in the second (old) edge
        city21, city22 = route[e2], route[(e2+1) % n]

        ## Costs of the old edges
        d1_old = dist[city11, city12] # first
        d2_old = dist[city21, city22] # second
        c_old = d1_old + d2_old       # total
        ## Costs of the new edges
        d1_new = dist[city11, city21]
        d2_new = dist[city12, city22]
        c_new = d1_new + d2_new
        ## Difference new - old
        delta_c = c_new - c_old
        return delta_c

    ## Make an entirely independent duplicate of the current object.
    def copy(self):
        return deepcopy(self)
