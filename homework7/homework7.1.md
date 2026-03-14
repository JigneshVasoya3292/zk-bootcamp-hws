**Problem 1**

Create a graph with 2 nodes and 1 edge and write constraints for a 3-coloring. Translate the 3-coloring to a rank-1 constraint system. (If you forgot how to do this, consult the chapter on arithmetic circuits.)

**Color validity (node constraint):**

```
(1 - n) * (2 - n) * (3 - n) === 0
```

Flatten to R1CS (one multiplication per row):

```
f === (1 - n) * (2 - n)
f * (3 - n) === 0
```

**No two same colors (edge constraint):** For adjacent nodes with colors x, y we need x ≠ y. Encode product constraint so valid pairs only:

```
(2 - xy) * (3 - xy) * (6 - xy) === 0
```

Introduce auxiliary variable u = xy, then flatten:

```
xy === u
(2 - u) * (3 - u) === w
w * (6 - u) === 0
```

- Each edge needs 3 multiplications; each node needs 2.
- For X ≠ Y we can use (X − Y) · Inv === 1 (with Inv as witness).
- The prime field must be larger than the max value of products (e.g. 9 for 3 colors), so reduction mod p doesn’t map distinct products to the same value. In F₇, 3·3 = 9 ≡ 2, which can collide with another valid product; with characteristic > 9 this collision is avoided.

---

**Problem 3**

Given an R1CS of the form

$$
L\,\vec{[s]_1} \odot R\,\vec{[s]_2} = O\,\vec{[s]_1} \odot \vec{[G_2]_2}
$$

where L, R, O are n×m matrices of field elements and **s** is a vector (encoded as G1 and G2 points),

write Python code that verifies the formula.

You can check equality of G12 elements in Python like this:

```python
a = pairing(multiply(G2, 5), multiply(G1, 8))
b = pairing(multiply(G2, 10), multiply(G1, 4))
eq(a, b)
```

**Hint:** Each row of the matrices corresponds to a separate pairing.

**Hint:** When **s** is given encrypted with both G1 and G2 generators, you don’t know whether they share the same discrete log. You can check that with an extra equation (e.g. a random linear combination in the exponent).

Solidity cannot multiply G2 points; do this assignment in Python.

---

**Problem 4**

Why does an R1CS require exactly one multiplication per row?

**Short answer:** To keep the system quadratic. With three factors (e.g. three multiplications) the constraint becomes cubic and is no longer representable as a single bilinear check. With two multiplications, e.g. x·y·z = 0, you cannot write it as (A·w)×(B·w) = C·w with one ×; you need a rank-2 (or higher) system, which is much harder to turn into a QAP (Quadratic Arithmetic Program).

### 1. The algebraic structure

**Rank-1** means each constraint is one bilinear equation:

$$
(A \cdot w) \times (B \cdot w) = C \cdot w
$$

- **w** = witness vector (all variables, e.g. n, f, u, w).
- **A, B, C** = row vectors (coefficients).
- **(A·w)** and **(B·w)** = linear combinations (only addition; no extra multiplication).
- The **×** is the single multiplication per row.

So x·y·z = 0 cannot be encoded in one rank-1 row; it would require rank-2 and complicates the QAP.

### 2. Efficiency in proofs

For **polynomial interpolation** we need a uniform shape:

1. **Flatten:** Express the circuit as many rows of the form A×B = C.
2. **Condense:** Interpolate these rows into polynomials.
3. **Prove:** Prover shows knowledge of a polynomial that vanishes on the constraint indices.

If some rows had one multiplication and others had two, the interpolating polynomial would not have a consistent degree, and the pairing-based check would break or become inefficient.

### 3. “Addition is free”

Inside (A·w) and (B·w) you can add arbitrarily many terms; that still counts as one “linear combination” and doesn’t add rows. Only the **one multiplication** between the two sides costs one R1CS row.

**Example:** f = (1−n)(2−n) is one row: A = (1−n), B = (2−n), C = f. Writing (1−n)(2−n)(3−n) = 0 in one row is impossible in rank-1 because that would be two multiplications.

### Relation to bilinear pairings

- R1CS is degree-2 because **bilinear pairings** only let us check one multiplication “in the exponent”: e([a]₁, [b]₂) = e([c]₁, [H]₂) checks a·b = c.
- Flattening to A×B = C is what makes this single multiplication check possible; higher-degree constraints would not fit the pairing equation.

**1. Hidden multiplication.** The prover sends commitments (e.g. elliptic curve points [A]₁, [B]₂). The verifier must check A·B = C but cannot multiply curve points directly. The bilinear map e satisfies e(g^a, g^b) = e(g,g)^{ab}, so the verifier can check the product in the exponent.

**2. Mapping R1CS to the pairing.** For a row (A·w)×(B·w) = C·w, with linear combinations a, b, c, the verifier checks e([a]₁, [b]₂) = e([c]₁, [H]₂). Bilinearity handles the linear combinations while enforcing the single multiplication per row.
