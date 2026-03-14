"""
R1CS in pairing form: L·[s]_1 ⊙ R·[s]_2 = O·[s]_1 ⊙ [G_2]_2
Verify by checking e((L·[s]_1)_i, (R·[s]_2)_i) = e((O·[s]_1)_i, G_2) for each row i.
"""

from py_ecc.bn128 import G1, G2, add, multiply, pairing, eq


def _scalar_vec(s, n):
    """Extract n scalars from s (column vector or flat list)."""
    out = []
    for i in range(n):
        si = s[i][0] if hasattr(s[i], "__getitem__") and not isinstance(s[i], int) else s[i]
        out.append(si)
    return out


def _matrix_times_vector_curve(M, vec_points, identity):
    """M @ vec: each row i is sum_j M[i][j] * vec[j] (group linear combination)."""
    m, n = len(M), len(M[0])
    result = []
    for i in range(m):
        acc = identity
        for j in range(n):
            acc = add(acc, multiply(vec_points[j], M[i][j]))
        result.append(acc)
    return result


def test_prob3(L, R, O, s):
    """
    L, R, O: n_constraints × n_vars matrices (list of lists of ints).
    s: witness column vector of length n_vars (list of scalars or n×1 list).
    Returns True iff L·[s]_1 ⊙ R·[s]_2 = O·[s]_1 ⊙ [G_2]_2 (pairing check per row).
    """
    m = len(L)
    n = len(L[0])
    if not (len(R) == m and len(R[0]) == n and len(O) == m and len(O[0]) == n):
        raise ValueError("L, R, O must be m×n with same dimensions")
    if len(s) < n:
        raise ValueError("s must have at least n elements")

    scalars = _scalar_vec(s, n)

    # [s]_1, [s]_2: vectors of G1 / G2 points
    s1 = [multiply(G1, scalars[j]) for j in range(n)]
    s2 = [multiply(G2, scalars[j]) for j in range(n)]

    # L·[s]_1, R·[s]_2, O·[s]_1 (each row = linear combination in the group)
    identity_g1 = multiply(G1, 0)
    identity_g2 = multiply(G2, 0)

    LS1 = _matrix_times_vector_curve(L, s1, identity_g1)
    RS2 = _matrix_times_vector_curve(R, s2, identity_g2)
    OS1 = _matrix_times_vector_curve(O, s1, identity_g1)

    # Verify: for each i, e(LS1[i], RS2[i]) == e(OS1[i], G2)
    for i in range(m):
        left = pairing(RS2[i], LS1[i])   # py_ecc pairing is e(G2, G1)
        right = pairing(G2, OS1[i])
        if not eq(left, right):
            return False
    return True


if __name__ == "__main__":
    # Example: 1 constraint, 2 vars. (1*s0 + 2*s1) * (3*s0 + 4*s1) = (5*s0 + 6*s1) in exponent.
    # Pick s = [1, 1]: L·s = 3, R·s = 7, O·s = 11. R1CS requires 3*7 = 21 = O·s, so O·s must be 21.
    # So use O such that O·[1,1]^T = 21, e.g. O = [[21, 0]].
    L = [[1, 2]]
    R = [[3, 4]]
    O = [[21, 0]]   # 21*1 + 0*1 = 21
    s = [[1], [1]]
    print("Valid R1CS (1*1+2*1=3, 3*1+4*1=7, 3*7=21):", test_prob3(L, R, O, s))

    # Invalid: same L, R, s but O·s = 0 (wrong)
    O_bad = [[0, 0]]
    print("Invalid R1CS (O·s != L·s * R·s):", test_prob3(L, R, O_bad, s))
