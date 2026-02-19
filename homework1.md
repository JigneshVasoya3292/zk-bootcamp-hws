# Homework 1

For all problems below, assume the finite field is p = 71.

**Remember, this is done in a finite field so your answer should only contain numbers [0-70] inclusive. There should be no fractions or negative numbers.**

The following Python code will be useful:

```python
>>> -5 % p # number congruent to -5
>>> pow(5, -1, p) # multiplicative inverse of 5
```

## Problem 1

Find the elements in a finite field that are congruent to the following values:

- -1 
70
- -4
67
- -160
53
- 500
3

## Problem 2

Find the elements that are congruent to a = 5/6, b = 11/12, and c = 21/12

a = 5/6 --> 11
Explanation : 
Multiplicative inverse of 6 (1/6) -> 6 * x = 1 
6 * 1 = 6 -> 6 % 71 = 6
6 * 2 = 12 -> 12 % 71 = 12
.
.
.
6 * 12 = 71 -> 72 % 71 = 1 
so 12 is multiplicative inverse of 6 in given field GF(71).
now, 5 * 12 = 60 -> 60 % 71 = 60 is congruent to 5/6.

b= 11/12 --> 
multiplicative inverse for 12 is 6. (12 * 6 % 71 = 1).
(11 * 6) % 71 = 66 is congruent to 11/12.

c = 21/12 -->
(21 * 6) % 71 = 55 is congruent to 21/12.

Verify your answer by checking that a + b = c (in the finite field)

60 + 66 (126 % 71) = 55

## Problem 3

Find the elements that are congruent to a = 2/3, b = 1/2, and c = 1/3.

1/3 -> 24
1/2 -> 36
a = 2/3 -> (2 * 24) % 71 = 48
b = 1/2 -> (36) % 71 = 36
c = 1/3 -> 24 % 71 = 24

Verify your answer by checking that a * b = c (in the finite field)

(48 * 36 = 1728 ) % 71 = 24
c = 24
a * b = c

## Problem 4

Note: if you forgot what a “matrix inverse” is, feel free to consult an AI first.

The inverse of a 2 x 2 matrix $A$ is

$$
A^{-1}=\frac{1}{\text{det}}\begin{bmatrix}d & -b\\-c & a\end{bmatrix}
$$

where $A$ is

$$
A = \begin{bmatrix}a & b\\c & d\end{bmatrix}
$$

And the determinant det is

$$
\text{det}=a \times d-b\times c
$$

Compute the inverse of the following matrix in the finite field:

$$
\begin{bmatrix}1 & 1\\1 & 4\end{bmatrix}
$$

Verify your answer by checking that

$$
AA^{-1}=I
$$

Where $I$ is the identity matrix.

Ainv = 1/3 * [[4 -1][-1 1]]

## Problem 5

What is the modular square root of 12?

Verify your answer by checking that x * x = 12 (mod 71)

Use brute force to find the answer (in Python)

15 * 15 = 225 % 71 = 12
so 15 & 56 (-15) are square modular square roots of 12