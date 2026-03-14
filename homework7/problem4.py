import numpy as np
import random

# u = !(x || (y && z)) || (x && !z)
#  y && z = y * z = v1
# x && !z = x * (1 - z) = v2
# u = !(x || v1) || v2
# !(x || v1) = !x && !v1 = (1 - x) * (1 - v1) = v3
# u = v3 || v2
# u = v3 + v2 - v3v2
#1. y * z = v1
#2. x * (1 - z) = v2
#3. (1 - x) * (1 - v1) = v3
#4. v3v2 = v3 + v2 - u
#5. x * (1 - x) = 0
#6. y * (1 - y) = 0
#7. z * (1 - z) = 0

# w = [1, x, y, z, v1, v2, v3, u]

P = 79

L = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [1, -1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0]])

R = np.array([[0, 0, 0, 1, 0, 0, 0, 0],
              [1, 0, 0, -1, 0, 0, 0, 0],
              [1, 0, 0, 0, -1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [1, -1, 0, 0, 0, 0, 0, 0],
              [1, 0, -1, 0, 0, 0, 0, 0],
              [1, 0, 0, -1, 0, 0, 0, 0]])

O = np.array([[0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 1, -1],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]])

def generate_witness(x, y, z):
    #1
    v1 = y * z
    v2 = x * (1 - z)
    v3 = (1 - x) * (1 - v1)
    u = v3 + v2 - v2 * v3
    w = [1, x, y, z, v1, v2, v3, u]
    return w

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