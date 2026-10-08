import numpy as np
import matplotlib.pyplot as plt

# create a grid of equally spaced angles between 0 and pi/2
# then compute cos and sin of them to find the coordinates of 
# equally spaced points on the quarter circle
num_points=100

# theta = [(np.pi/2) / (num_points-1) * i for i in range(num_points)] #list of angles
# xs = [] 
# ys = []
# for t in theta:
#     x = np.cos(t)
#     y = np.sin(t)
#     xs.append(x)
#     ys.append(y)
    
theta = np.linspace(0., np.pi/2, num_points)
xs = np.cos(theta)
ys = np.sin(theta)
    
plt.clf()
plt.plot(xs, ys, color="red")


n_mc = 1000 # number of mc points

# write a for loop 
# generate the point: x and y coordinates
# see if the point falls inside
# count it if it does
# compute the estimation of pi
# print it

# ninside = 0
# for i in range(n_mc):
#     px = np.random.random()
#     py = np.random.random() 
#     # if np.sqrt(px**2 + py**2) <= 1:
#     if px**2 + py**2 <= 1:
#         ninside += 1


ninside = 0
# pxs = []
# for i in range(n_mc):
#     px = np.random.random()
#     pxs.append(px)
# pys = []
# for i in range(n_mc):
#     py = np.random.random() 
#     pys.append(py)

pxs = np.random.random(n_mc)
pys = np.random.random(n_mc)

# for i in range(n_mc):
#     px = pxs[i]
#     py = pys[i]
#     if px**2 + py**2 <= 1:
#         ninside += 1


ninside = np.sum(pxs**2 + pys**2 <= 1)
        
print(f"estimated pi = {4* ninside / n_mc} real pi = {np.pi}")

plt.plot(pxs, pys, ".", color="blue")
plt.show()
# plt.scatter(pxs, pys, color="blue")


## TASKS
# 1. Complete the plot by drawing also the square (in black), in a single line
# 2. Generalize the pi estimation with MC to high-dimensions
# 3. Scaling analysis
# 4. Only plot the mc points that fall inside the circle
