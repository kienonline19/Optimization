import numpy as np


# generate a random initial marginal probability distribution
# generate a random stochastic process -> random stochastic matrix Q
# show that by iterating the transition law we converge to a stationary distribution 
# show that this stationary distribution does not depend on the initial condition


M = 20


def create_random_marginal(M):
    p = np.random.rand(M) # = rho in the slides
    # make sure the entries sum to 1
    p = p / np.sum(p) # broadcasting trick
    return p


def create_Q(M):
    Q = np.random.rand(M,M)
    # check normalization to 1
    Q = Q / Q.sum(axis=0) # broadcasting trick
    return Q

# sample from a given marginal p
Q = create_Q(M)
p = create_random_marginal(M)
for i in range(1000):
    p = Q @ p
# now p is the stationary distribution for Q


np.random.choice(np.arange(M), p = p)


# alternative way of sampling
# use the stochastic process Q

def markov_chain(Q, p0=None, max_iters=10000):
    # initialize the markov chain -> choose initial state
    if p0 is None:
        x = 0
    else:
        x = np.random.choice(np.arange(M), p=p0)
        
    for t in range(max_iters):
        # Q[:,i] probability of jumping from i to anywhere else
        # move proposal 
        y = np.random.choice(np.arange(M), p=Q[:,x])
        # move acceptance
        x = y
        
    return x









