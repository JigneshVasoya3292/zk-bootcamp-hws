**Problem 1**

Create a graph with 2 nodes and 1 edge and write constraints for a 3-coloring. T the 3-coloring to a rank 1 constraint system. If you forgot how to do this, consult the chapter on arithmetic circuits.

color validity constraint, node constraint
(1 - n) * (2 - n) * (3 - n) === 0

f === (1 - n) * (2 - n)
f * (3 - n) === 0 (R1CS)

no 2 same color constraint, edge constraint

(2 - xy) * (3 - xy) * (6 - xy) === 0

xy === u
(2 - u) * (3 - u) = w
w * (6 - u) === 0 (R1CS)

each edge needs 3 multiplication, each node required 2
for X != Y,
(X - y) * Inv === 1

But prime field should be greater than max of x*y (9 in above case), so that
mod doesn't round to a valid x*y value.

With F7, 3 * 3 = 9 mod 7 = 2 which is a valid value, 
If prime field has characteristics is greater than 9, this won't happen.

**Problem 2**

Write python code that takes an R1CS matrix A, B, and C and a witness vector w and
verifies.

*Aw* ⊙ *Bw* − *Cw* = 0

Where ⊙ is the hadamard (element-wise) product.

Use this to code to check your answer above is correct.