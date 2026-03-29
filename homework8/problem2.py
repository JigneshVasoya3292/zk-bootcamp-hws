import galois
import numpy as np
import random
from scipy.interpolate import lagrange


def matrix_to_poly(A, v):
    # A, B are n * m matrix
    matrix = np.array(A)
    n = len(A)
    m = len(A[0])
    result = []
    xs = []
    poly = 0
    
    for i in range(m):
        xs.append(i+1)
    
    for i in range(m):
        col_poly = lagrange(xs, matrix[:,i])
        result.append(col_poly)
    
    for i in range(m):
        poly = poly + result[i]*v[i]

    return poly

polyA = matrix_to_poly([[9, 4, 5], [8, 3, 4], [7, 9, 11]], [1, 3, 7])
polyB = matrix_to_poly([[2, 4, 6], [1, 3, 5], [7, 9, 11]], [1, 3, 7])

x = random.randint(1, 2**10)
print(x)
print(polyA)
print(polyB)
print(polyA(x) == polyB(x))
    