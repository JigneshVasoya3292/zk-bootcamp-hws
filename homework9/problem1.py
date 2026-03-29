import numpy as np
import random
from scipy.interpolate import lagrange

# Define the matrices
A = np.array([[0,0,3,0,0,0],
               [0,0,0,0,1,0],
               [0,0,1,0,0,0]])

B = np.array([[0,0,1,0,0,0],
               [0,0,0,1,0,0],
               [0,0,0,5,0,0]])

C = np.array([[0,0,0,0,1,0],
               [0,0,0,0,0,1],
               [-3,1,1,2,0,-1]])

# pick values for x and y
x = 100
y = 100

# this is our orignal formula
out = 3 * x * x * y + 5 * x * y - x- 2*y + 3# the witness vector with the intermediate variables inside
v1 = 3*x*x
v2 = v1 * y
w = np.array([1, out, x, y, v1, v2])

result = C.dot(w) == np.multiply(A.dot(w),B.dot(w))
assert result.all(), "result contains an inequality"

# QAP conversion
# l(x) * r(x) = O(x)

# For A
a1 = [0, 0, 0] # column 0
a2 = [0, 0, 0] # column 1
a3 = [3, 0, 1] # column 2
a4 = [0, 0, 0] # column 3
a5 = [0, 1, 0] # column 4
a6 = [0, 0, 0] # column 5

xs = [0, 1, 2] # 3 rows, so 0, 1,2 for x values

a1x = lagrange(xs, a1)
print(a1x) # y = 0

a2x = lagrange(xs, a2)
print(a2x) # y = 0

a3x = lagrange(xs, a3)
print(a3x) # y = 2 x^2 - 5 x + 3

a4x = lagrange(xs, a4)
print(a4x) # y = 0

a5x = lagrange(xs, a5)
print(a5x) # y = -x^2 + 2 x

a6x = lagrange(xs, a6)
print(a6x) # y = 0

# For B
b1 = [0, 0, 0] # column 0
b2 = [0, 0, 0] # column 1
b3 = [1, 0, 0] # column 2
b4 = [0, 1, 5] # column 3
b5 = [0, 0, 0] # column 4
b6 = [0, 0, 0] # column 5

b1x = lagrange(xs, b1)
print(b1x) # y = 0

b2x = lagrange(xs, b2)
print(b2x) # y = 0

b3x = lagrange(xs, b3)
print(b3x) # y = 0.5 x^2 - 1.5 x + 1

b4x = lagrange(xs, b4)
print(b4x) # y = 1.5 x^2 - 0.5x

b5x = lagrange(xs, b5)
print(b5x) # y = 0

b6x = lagrange(xs, b6)
print(b6x) # y = 0

# For C
c1 = [0, 0, -3] # column 0
c2 = [0, 0, 1] # column 1
c3 = [0, 0, 1] # column 2
c4 = [0, 0, 2] # column 3
c5 = [1, 0, 0] # column 4
c6 = [0, 1, -1] # column 5

c1x = lagrange(xs, c1)
print(c1x) # y = -1.5 x^2 + 1.5x

c2x = lagrange(xs, c2)
print(c2x) # y = 0.5 x^2 - 0.5x

c3x = lagrange(xs, c3)
print(c3x) # y = 0.5 x^2 - 0.5x

c4x = lagrange(xs, c4)
print(c4x) # y = x^2 - x

c5x = lagrange(xs, c5)
print(c5x) # y = 0.5 x^2  - 1.5x + 1

c6x = lagrange(xs, c6)
print(c6x) # y = -1.5 x^2 + 2.5x

#l(x) = a1x * w1 + a2x * w2 + a3x * w3 ....  w is witness
lx = 1 * a1x + out * a2x + x * a3x + y * a4x + v1 * a5x + v2 * a6x
print(lx) # -29800 x^2 + 59500 x + 300

rx = 1 * b1x + out * b2x + x * b3x + y * b4x + v1 * b5x + v2 * a6x
print(rx) # 200 x^2 - 200x + 100

ox = 1 * c1x + out * c2x + x * c3x + y * c4x + v1 * c5x + v2 * c6x
print(ox) # -2960000 x^2 + 5930000 x + 30000

# for x = 0, lx * rx = ox --> 3*x*x = v1
# 300 * 100 = 30000

# for x = 1, lx * rx = ox, --> v1 * y = v2
# (-29800 + 59500 + 300) = 30000
# (200 - 200 + 100) = 100 
# (30000) * (100) = 3000000
# -2960000 + 5930000 + 30000 = 3000000

# for x = 2, lx * rx = ox --> x * 5y = out - v2 + x + 2*y - 3
# (-29800 * 2 * 2 + 59500 * 2 + 300) = 100
# (200 * 2 * 2 - 200 * 2 + 100) = 500
# (100) * (500) = 500
# -29600 * 2 * 2 + 5930000 * 2 + 30000 = 50000