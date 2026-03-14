import numpy as np
import random

# 3xy - x^2 = 2xz - z^2
# -x^3 = 4x - zy - 1/2
#
#1. x^2 = v1
#2. z^2 = v2
#3. xy - v3
#4. 3v3 - v1 + v2 = 2xz
#5. 4 + v1 = v4
#6. zy = v5
#7. 1 + 2*v5 = 2x * v4

# w = [1, x, y, z, v1, v2, v3, v4]

P = 79

def mod_inv(n, p):
    # Fermat's Little Theorem for modular inverse: n^(p-2) % p
    return pow(n, p - 2, p)

def generate_witness(x, y, u, t):
    # 1. Start with the constant 1
    one = 1
    
    # 2. Calculate intermediate variables based on our constraints
    # Constraint: w1 = t * u
    w1 = (t * u) % P
    
    # Constraint: w2 = v * x
    # Note: From our 2nd equation: v = t*u + 2vx + 3
    # v = w1 + 2*v*x + 3  =>  v - 2vx = w1 + 3  =>  v(1 - 2x) = w1 + 3
    # So v = (w1 + 3) / (1 - 2*x)
    # numerator: (w1 + 3)
    num = (w1 + 3) % P
    # denominator: (1 - 2x)
    den = (1 - 2 * x) % P
    
    if den == 0:
        raise ValueError("Division by zero in field! Choose a different x.")
    
    v = (num * mod_inv(den, P)) % P
    
    # 4. Intermediate: w2 = v * x
    w2 = (v * x) % P
    
    # Constraint: w3 = x * (y + u) AND w3 = z * v
    # We'll use x * (y + u) to define it
    w3 = (x * (y + u)) % P
    
    z = (w3 * mod_inv(v, P)) % P
    
    # Validation check: Since z is an input, we ensure z * v == w3
    if (z * v) % P != w3:
        print(f"Warning: Input 'z' ({z}) does not satisfy z*v = w3 mod 79")
        print(f"Required z would be: {(w3 * mod_inv(v, P)) % P}")
    
    # 3. Construct the vector s in the exact order of our matrices:
    # [1, x, y, u, v, z, t, w1, w2, w3]
    witness = [one, x, y, z, t, u, v, w1, w2, w3]
    
    return witness

L = np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [3, 0, 0, 0, 0, 0, 0, 1, 2, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]])

R = np.array([[0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]])

O = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

x = random.randint(1, P-1)
y = random.randint(1, P-1)
t = random.randint(1, P-1)
u = random.randint(1, P-1)

w = generate_witness(x, y, u, t)

left = L.dot(w) % P
right = R.dot(w) % P
lr = np.multiply(left, right) % P
o = O.dot(w) % P
result = o == lr
print(w)
print(o)
print(lr)
assert result.all(), "result contains an inequality"


