import galois
import numpy as np
import random
from scipy.interpolate import lagrange

P = 109
GFP = galois.GF(P)

def create_polynomials(A, B):
    xs = GFP(np.array(A))
    ys = GFP(np.array(B))
    
    # we can check that the coefficients with lagrange = lagrange_poly over a field
    # print(lagrange(A, B)) 
    
    p = galois.lagrange_poly(xs, ys)
    return p

print(create_polynomials([1,2,3,4], [4,8,2,1]))