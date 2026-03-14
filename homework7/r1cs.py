"""
R1CS test case generator and verifier.
Constraint: Aw ⊙ Bw − Cw = 0  (element-wise product, over a prime field F_p)
"""

import numpy as np

def test_r1cs(A, B, C, w, p=None):
    """Check Aw ⊙ Bw − Cw = 0. If p is given, arithmetic is mod p."""
    aw = A @ w
    bw = B @ w
    cw = C @ w
    if p is not None:
        aw = aw % p
        bw = bw % p
        cw = cw % p
    aw_bw = np.multiply(aw, bw)
    if p is not None:
        aw_bw = aw_bw % p
    diff = aw_bw - cw
    if p is not None:
        diff = diff % p
    return np.all(diff == 0)


def generate_testcases(n_constraints=3, n_vars=4, p=97, seed=None):
    """
    Generate A, B, C (n_constraints × n_vars) and w (n_vars) over F_p
    such that Aw ⊙ Bw − Cw = 0.
    """
    if seed is not None:
        np.random.seed(seed)
    # Random witness; ensure w[0] != 0 so we can solve for C easily
    w = np.random.randint(1, p, size=n_vars, dtype=np.int64)
    # Random A, B
    A = np.random.randint(0, p, size=(n_constraints, n_vars), dtype=np.int64)
    B = np.random.randint(0, p, size=(n_constraints, n_vars), dtype=np.int64)
    aw = (A @ w) % p
    bw = (B @ w) % p
    target = (aw * bw) % p  # Cw must equal this
    # C such that C @ w = target: set C[i, 0] = target[i] * inv(w[0]) mod p, rest 0
    w0_inv = pow(int(w[0]), -1, p)
    C = np.zeros((n_constraints, n_vars), dtype=np.int64)
    C[:, 0] = (target * w0_inv) % p
    return A, B, C, w, p


def generate_simple_testcase(p=97):
    """Simple hand-checkable test case: 1 constraint, small numbers."""
    # e.g. (2*w0 + w1) * (w0 + 3*w1) = 2*w0 + 7*w1 + 3*w2 (we choose w so it holds)
    # Pick w = [1, 1, 0]. Then Aw = 2+1=3, Bw = 1+3=4, so Aw*Bw = 12. We need Cw = 12.
    # So C = [12, 0, 0] gives Cw = 12. OK.
    A = np.array([[2, 1, 0]])
    B = np.array([[1, 3, 0]])
    w = np.array([1, 1, 0])
    aw = A @ w
    bw = B @ w
    C = np.array([[aw[0] * bw[0], 0, 0]])  # Cw = 12
    return A, B, C, w, None


if __name__ == "__main__":
    # Integer (no field)
    A, B, C, w, _ = generate_simple_testcase()
    print("Simple test case (integers):")
    print("A =\n", A)
    print("B =\n", B)
    print("C =\n", C)
    print("w =", w)
    print("Aw ⊙ Bw − Cw = 0:", test_r1cs(A, B, C, w))

    # Over F_p
    A, B, C, w, p = generate_testcases(n_constraints=4, n_vars=5, p=97, seed=42)
    print("\nRandom test case (mod {}):".format(p))
    print("A =\n", A)
    print("B =\n", B)
    print("C =\n", C)
    print("w =", w)
    print("Aw ⊙ Bw − Cw ≡ 0 (mod {}):".format(p), test_r1cs(A, B, C, w, p))

