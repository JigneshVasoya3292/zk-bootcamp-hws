# Homework 8

Use these for code references:

https://www.rareskills.io/post/python-lagrange-interpolation
https://www.rareskills.io/post/schwartz-zippel-lemma

## Problem 1

Alice and Bob have two vectors, and they want to test if they are the same vector. Assume that they evaluate their polynomials honestly. Write the code they would use to turn their vector into a polynomial over a finite field.

## Problem 2

Alice and Bob have matrices $\mathbf{A}$ and $\mathbf{B}$. They want to know if, for some $\mathbf{v}$ that

$$
\mathbf{A}\mathbf{v}=\mathbf{B}\mathbf{v}
$$

Here, the matrices $\mathbf{A}$ and $\mathbf{B}$ have $n$ rows and $m$ columns.

For example, let

$$
\mathbf{A}=\begin{pmatrix}9&4&5\\8&3&4\\7&9&11\end{pmatrix}
$$

$$
\mathbf{B}=\begin{pmatrix}2&4&6\\1&3&5\\7&9&11\end{pmatrix}
$$

$$
\mathbf{v}=\begin{pmatrix}1\\3\\7\end{pmatrix}
$$

Alice and Bob could compute and publish $\mathbf{A}\mathbf{v}$ and $\mathbf{B}\mathbf{v}$ respectively, but that would not be succinct.

Instead, Alice and Bob doe Lagrange interpolation on the columns of $\mathbf{A}$ and $\mathbf{B}$, turning them into $m$ polynomials. That is, $\mathbf{A}$ gets turned into

$$
u_1(x),u_2(x),u_3(x)
$$

and $\mathbf{B}$ gets turned into 

$$
v_1(x),v_2(x),v_3(x)
$$

Each of the $u_1...u_3$ are polynomials formed by taking a column from the matrix and running lagrange interpolation on it against xs = [1,2,3]. For example, $u_1(x)$ is computed as:

$$
u_1=\texttt{lagrange}([1,2,3],[9,8,7])
$$

Alice can turn the three polynomials into a single polynomial by doing:

$$
a(x)=u_1(x)v_1+u_2(x)v_2+u_3(x)v_3
$$

In the example above, $v_1=1$, $v_2=3$, $v_3=7$. Now Alice has turned her matrix and vector into a single polynomial.

Bob can compute a single polynomial in the same manner.

They can then check that the polynomials created below are equal by using the Schwart-Zippel Lemma as before:

$$
\underbrace{1\cdot u_1(x)+3\cdot u_2(x)+7\cdot u_3(x)}_\text{Alice}=\underbrace{1\cdot v_1(x)+3\cdot v_2(x)+7\cdot v_3(x)}_\text{Bob}
$$

Do not worry for now about whether they do their computations honestly.

Write code that will accomplish this algorithm for arbitrary-sized matrices of reasonable size.