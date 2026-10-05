import numpy as np
import matplotlib.pyplot as plt


def display(grid_size, pos):
    # clear the plot
    plt.clf()
    
    # plot the grid lines
    for i in range(grid_size):
        plt.plot([0, grid_size-1], [i,i], color="black") # plotting a row in the grid
        plt.plot([i,i], [0, grid_size-1], color="black") # plotting a column in the grid
    
    # plot the walkers
    plt.plot(pos[:,1], pos[:,0], "o", color="blue")
    plt.show()
    plt.pause(0.0001) # take some time to do the plot
        

def random_walks(grid_size, num_walkers=1, steps=100):
    
    # define possible moves and probabilities
    moves = np.array([[0,1], [0,-1], [1,0], [-1,0]])
    prob = np.ones(len(moves)) / len(moves)
    
    # initialize the positions
    pos = np.zeros((num_walkers, 2), dtype=int)
    pos[:,:] = grid_size // 2 # start everyone in the middle of the grid
    
    for i in range(steps):
        # propose move (and accept!)
        for j in range(num_walkers):
            m = moves[np.random.choice(len(moves), p=prob)]
            pos[j, :] += m
        # TASK: vectorize this! (avoid the for loop)   
        
        pos %= grid_size # restrict in the interval {0,...,n-1} -> periodic boundary conditions
        
        # display!
        display(grid_size, pos)
        
    return pos

    