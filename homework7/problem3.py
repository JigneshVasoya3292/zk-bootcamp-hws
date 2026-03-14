import numpy as np
import random

# Write a set of constraints that models u = x && y && !z. Don’t forget the $\set{0,1}$ constraints.

# x && y === xy
# !z === (1 - z)
# u = xy * (1 - z)
#1. x*(x-1) = 0
#2. y*(y-1) = 0
#3. z*(z-1) = 0
#4. xy = v1
#5. v1 * (1 - z) = u
#6. x*(1 - x) = 0
#7. y*(1 - y) = 0
#8. z*(1 - z) = 0

# w = [1 x y z u v1]
P = 79

def generate_witness(x, y, z):
    v1 = x*y
    u = v1 * (1-z)
    w = [1, x, y, z , u, v1]
    return w

L = np.array([[0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0]])
R = np.array([[-1, 1, 0, 0, 0, 0],
              [-1, 0, 1, 0, 0, 0],
              [-1, 0, 0, 1, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [1, 0, 0, -1, 0, 0],
              [1, -1, 0, 0, 0, 0],
              [1, 0, -1, 0, 0, 0],
              [1, 0, 0, -1, 0, 0]])
O = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]])

x = 1
y = 1
z = 0
w = generate_witness(x, y, z)

left = L.dot(w) % P
right = R.dot(w) % P
lr = np.multiply(left, right) % P
o = O.dot(w) % P
result = o == lr
print(w)
print(o)
print(lr)
assert result.all(), "result contains an inequality"