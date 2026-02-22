

from py_ecc.bn128 import G1, add, multiply, neg, curve_order
import secrets

num = 205
den = 421
# P + Q = T
# T = num/den = den^-1 * num 


den_inv = pow(den , -1 , curve_order)
tg_scalar = (den_inv * num ) % curve_order

target_point = multiply(G1, tg_scalar)

# random scalar k
r = secrets.randbelow(curve_order)
P = multiply(G1, r)

#Q = T + (-P)
Q = add(target_point, neg(P))

result = add(P, Q)
print(f"Match: {result == target_point}")
print(f"P: {P} \n Q: {Q} \n num: {num} \n den: {den}")