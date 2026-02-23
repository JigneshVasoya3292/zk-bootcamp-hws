"""Generate testcase data for homework5 (rational add + matrix multiplication)."""

from py_ecc.bn128 import G1, add, multiply, neg, curve_order
import secrets
import random
import json


def generatepoints():
    num = 205
    den = 421
    # P + Q = T; T = num/den
    den_inv = pow(den, -1, curve_order)
    tg_scalar = (den_inv * num) % curve_order
    target_point = multiply(G1, tg_scalar)

    r = secrets.randbelow(curve_order)
    P = multiply(G1, r)
    Q = add(target_point, neg(P))

    result = add(P, Q)
    print(f"Match: {result == target_point}")
    print(f"P: {P} \n Q: {Q} \n num: {num} \n den: {den}")


def generate_matrix_testcase(n: int = 3, matrix: list[list[int]] | None = None, seed: int | None = None):
    """
    Generate (matrix M, points s, scalars o) such that M*s = o (as EC: M·s_i = o_i*G).
    s[i] = k[i]*G, o = M*k (mod curve_order).
    """
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert len(matrix) == n and all(len(row) == n for row in matrix), "matrix must be n×n"

    if seed is not None:
        random.seed(seed)

    def rand_scalar():
        if seed is not None:
            return random.randint(0, curve_order - 1) if curve_order > 0 else 0
        return secrets.randbelow(curve_order)

    k = [rand_scalar() for _ in range(n)]

    # s[i] = k[i] * G
    s_points = [multiply(G1, ki) for ki in k]

    # o[i] = (M * k)[i] mod curve_order
    o = []
    for i in range(n):
        oi = sum(matrix[i][j] * k[j] for j in range(n)) % curve_order
        o.append(oi)

    return matrix, s_points, o


def print_matrix_testcase_solidity(n: int = 3, matrix: list[list[int]] | None = None, seed: int | None = None):
    """Print testcase in Solidity-friendly form for copy-paste into tests."""
    matrix, s_points, o = generate_matrix_testcase(n=n, matrix=matrix, seed=seed)

    # Solidity matrix literal (uint256[][])
    rows = ", ".join(f"[{', '.join(str(m) for m in row)}]" for row in matrix)
    print("// Matrix M (n×n)")
    print(f"uint256[][] memory matrix = new uint256[][]({n});")
    for i, row in enumerate(matrix):
        print(f"matrix[{i}] = [{', '.join(str(x) for x in row)}];")

    print("\n// ECPoint[] s (n points, s[i] = k[i]*G)")
    print("ECPoint[] memory s = new ECPoint[](n);")
    for i, p in enumerate(s_points):
        print(f"s[{i}] = ECPoint({{ x: {p[0]}, y: {p[1]} }});")

    print("\n// uint256[] o (M*k mod curve_order)")
    print(f"uint256[] memory o = [{', '.join(str(x) for x in o)}];")

    print("\nassertTrue(matrixMul.matrixmul(matrix, n, s, o));")


def print_matrix_testcase_json(n: int = 3, matrix: list[list[int]] | None = None, seed: int | None = None):
    """Print testcase as JSON for programmatic use."""
    matrix, s_points, o = generate_matrix_testcase(n=n, matrix=matrix, seed=seed)
    s_list = [{"x": str(p[0]), "y": str(p[1])} for p in s_points]
    out = {
        "n": n,
        "matrix": matrix,
        "s": s_list,
        "o": [str(x) for x in o],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    import sys

    # python testcases.py matrix 1000000000000000000000000000000000000000000000000000000000000000 json
    if len(sys.argv) > 1 and sys.argv[1] == "matrix":
        seed = int(sys.argv[2]) if len(sys.argv) > 2 else None
        fmt = sys.argv[3] if len(sys.argv) > 3 else "solidity"
        n = 3
        if fmt == "json":
            print_matrix_testcase_json(n=n, seed=seed)
        else:
            print_matrix_testcase_solidity(n=n, seed=seed)
    else:
        generatepoints()