import numpy as np
import galois
from scipy.interpolate import lagrange
# z = x^4 - 5y^2 x^2

#constraints
# v1 = x*x 
# v2 = v1 * v1 // x^4 
# v3 = y*y 
# z = v2 - 5v3 * v1
# 5v3 * v1 = v2 - z

x = 4
y = -2
v1 = x*x
v2 = v1*v1
v3=y*y
z = v2 - 5*v3*v1

# constraints
# x*x = v1
# v1*v1 = v2
# y*y = v3
# 5v3 * v1 = v2 - z
w = np.array([1, x, y, z, v1, v2, v3])
L = np.array([[0,1,0,0,0,0,0],
     [0,0,0,0,1,0,0],
     [0,0,1,0,0,0,0],
     [0,0,0,0,0,0,5]])

R = np.array([[0,1,0,0,0,0,0],
     [0,0,0,0,1,0,0],
     [0,0,1,0,0,0,0],
     [0,0,0,0,1,0,0]])

O = np.array([[0,0,0,0,1,0,0],
     [0,0,0,0,0,1,0],
     [0,0,0,0,0,0,1],
     [0,0,0,-1,0,1,0]])

result = O.dot(w) == np.multiply(L.dot(w),R.dot(w)) # without Field 79
assert result.all(), "result contains an inequality" 

P=79
GF = galois.GF(P)

# convert negative values to valid values over Field 79
L = L % P
R = R % P
O = O % P

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

x = 4
y = -2 % P
v1 = (x*x) % P
v2 = (v1 * v1 ) % P
v3 = (y*y) % P
z = (v2 - 5*v3*v1) % P

w = GF(np.array([1, x, y, z, v1, v2, v3 ]))

result = O_galois.dot(w) == np.multiply(L_galois.dot(w),R_galois.dot(w))
assert result.all(), "result contains an inequality, galois"

def lagrange_poly(col):
    xs = GF(np.array([0, 1, 2, 3])) # 4 rows
    return galois.lagrange_poly(xs, col)

# axis = 0, takes column, does lagrange polynomail for each column
U_Poly = np.apply_along_axis(lagrange_poly, 0, L_galois)
V_Poly = np.apply_along_axis(lagrange_poly, 0, R_galois)
W_Poly = np.apply_along_axis(lagrange_poly, 0, O_galois)

print(U_Poly)
print(V_Poly)
print(W_Poly)

def poly_into_witness(poly, witness) :
    n = len(poly)
    poly_sum = GF(0)
    for i in range (n):
        poly_sum = poly_sum + poly[i] * witness[i]
    return poly_sum

lx = poly_into_witness(U_Poly, w)
rx = poly_into_witness(V_Poly, w)
ox = poly_into_witness(W_Poly, w)

print(lx)
print(rx)
print(ox)

#lx = 38 x^3 + 29 x^2 + 24x + 4
#rx = 11 x^3 + 31 x^2 + 49x + 4
#ox = 45 x^3 + 13 x^2 + 23x + 16

# for x = 0
# lx = 4, rx = 4
# lx * rx = 16 % 79 = 16
# ox = 16 

# for x = 1
# lx = 95, rx = 95
# lx*rx = 9025 % 79 = 19
# ox = 98 % 79 = 19

# for x = 2
# lx = 472, rx = 314
# lx*rx = 148208 % 79 = 4
# ox = 478 % 79 = 4

# for x=3
# lx = 1363, rx = 727
# lx * rx = 4
# ox = 1426 % 79 = 4


