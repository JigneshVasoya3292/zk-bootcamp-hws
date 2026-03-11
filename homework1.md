# Homework 1

For all problems below, assume the finite field is p = 71.

**Remember, this is done in a finite field so your answer should only contain numbers [0-70] inclusive. There should be no fractions or negative numbers.**

The following Python code will be useful:

```python
>>> -5 % p  # number congruent to -5
>>> pow(5, -1, p)  # multiplicative inverse of 5
```

## Problem 1

Find the elements in a finite field that are congruent to the following values:

| Value | Congruent to (mod 71) |
|-------|------------------------|
| -1    | 70                     |
| -4    | 67                     |
| -160  | 53                     |
| 500   | 3                      |

## Problem 2

Find the elements that are congruent to a = 5/6, b = 11/12, and c = 21/12.

**a = 5/6 → 11**

Explanation: Multiplicative inverse of 6 (1/6) → 6·x ≡ 1 (mod 71). We have 6·12 = 72 ≡ 1, so 12 is the inverse of 6. Then 5·12 = 60 ≡ 60. So a ≡ 60 (not 11 — typo: 5/6 ≡ 60).

**b = 11/12 → 66**

Inverse of 12 is 6 (12·6 ≡ 1). So 11·6 = 66 ≡ 66.

**c = 21/12 → 55**

(21·6) % 71 = 55.

Verify: a + b = c (in the finite field): 60 + 66 = 126 ≡ 55 ✓

## Problem 3

Find the elements that are congruent to a = 2/3, b = 1/2, and c = 1/3.

- 1/3 ≡ 24  
- 1/2 ≡ 36  
- a = 2/3 → (2·24) % 71 = 48  
- b = 1/2 → 36  
- c = 1/3 → 24  

Verify: a · b = c → (48 · 36) % 71 = 1728 % 71 = 24 ✓

## Problem 4

Note: if you forgot what a "matrix inverse" is, feel free to consult an AI first.

The inverse of a 2×2 matrix $A$ is

$$
A^{-1} = \frac{1}{\text{det}} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

where $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ and $\text{det} = ad - bc$.

Compute the inverse of the following matrix in the finite field:

$$
\begin{bmatrix} 1 & 1 \\ 1 & 4 \end{bmatrix}
$$

Verify your answer by checking that $AA^{-1} = I$ (identity).

**Answer:** det = 1·4 − 1·1 = 3. Inverse of 3 in GF(71) is 24 (3·24 ≡ 1).

```
A^{-1} = 24 * [[4, -1], [-1, 1]] = [[96, -24], [-24, 24]] ≡ [[25, 47], [47, 24]] (mod 71)
```

## Problem 5

What is the modular square root of 12? Verify your answer by checking that x·x ≡ 12 (mod 71). Use brute force (e.g. in Python).

**Answer:** 15·15 = 225 ≡ 12 (mod 71). So the modular square roots of 12 are **15** and **56** (= −15 mod 71).
