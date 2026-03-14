# R1CS Practice

For all of the problems below, do it in a finite field modulo 79. All numbers should be in the range [0, 78] and there shouldn’t be any subtractions or fractions in the final result (use the additive inverse and multiplicative inverse instead).

1. Convert the following set of constraints to R1CS

$$
\begin{align*}
z*v &= x*y+x*u\\
v &= t*u + 2*v*x + 3
\end{align*}
$$

1. Convert the set of constraints to R1CS.

$$
\begin{align*}
3*x*y - x^2 &= 2x*z-z^2\\
-x^3 &= 4x - z*y - \frac{1}{2}  
\end{align*}
$$

1. Write a set of constraints that models `u = x && y && !z`. Don’t forget the $\set{0,1}$ constraints.

1. Write a set of constraints that models `u = !(x || (y && z)) || (x && !z)`. Don’t forget the $\set{0,1}$ constraints. Convert that to a R1CS.