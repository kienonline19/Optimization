# check the computational gain of employing ndarrays instead of lists
# sum random numbers

import random 
import time
import numpy as np
import numpy.random as rnd

n = 1000000

t0 = time.time()
l = [random.random() for i in range(n)]
t1 = time.time() 
print(f"python list creation time t={t1 - t0}")


t0 = time.time()
a = rnd.rand(n)
t1 = time.time() 
print(f"numpy array creation time t={t1 - t0}")

# sum up all the entries in the python list and measure how much time it takes


t0 = time.time()
s_list = sum(l)
t1 = time.time() 
print(f"python list sum time t={t1 - t0}")



t0 = time.time()
# s_array = np.sum(a)
s_array = a.sum()
t1 = time.time() 
print(f"numpy array sum time t={t1 - t0}")
