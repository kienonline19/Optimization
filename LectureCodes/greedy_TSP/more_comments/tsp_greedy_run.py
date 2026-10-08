## Example script

## Load the two modules, one for the generic optimizer and the other for a
## particular problem that we want to solve.
## These correspond to the file names (minus the .py extension). Module names
## are usually capitalized. Python looks for them in the current working
## directory (and if it doesn't find them, in some other default locations
## that it knows about, for example those where the packages are installed,
## like numpy and matplotlib...)
import Greedy
import TSP

## Generate a problem to solve.
## The first TSP is the name of the module, the second one is the name of the
## class.
tsp = TSP.TSP(100, seed=456329)

## Now we optimize it. Again, name_of_the_module.name_of_the_function
best = Greedy.greedy(tsp, num_iters = 50000, repeats = 30,
                     debug_delta_cost = False) # set to True to enable the check
