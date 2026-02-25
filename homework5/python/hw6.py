from py_ecc.bn128 import G1, G2, add, multiply, neg, pairing

A1 = multiply(G1, 4)
B2 = multiply(G2, 113)
x1 = 4
x2 = 5
x3 = 12

print(f"A1 : {A1}")
print(f"B1 : {B2}")

alpha1 = multiply(G1, 5)
beta2 = multiply(G2, 6)
gamma2 = multiply(G2, 7)
C1 = multiply(G1, 11)
delta2 = multiply(G2, 25)

X1 = add(multiply(G1, x1), add(multiply(G1, x2), multiply(G1, x3)))

pair1 = pairing(beta2, alpha1)
pair2 = pairing(gamma2, X1)
pair3 = pairing(delta2, C1)

lhs = pairing(B2, A1)
rhs = pair1 * pair2 * pair3

print(f"lhs = rhs is {lhs == rhs}");
