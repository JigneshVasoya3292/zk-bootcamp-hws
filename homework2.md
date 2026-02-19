# Homework 2

Magma = Closed
Semigroup = Closed, Associative
Monoid = Closed, Associative, Identity Element (e)
Group = Closed, Associative , Identity Element , Inverse
Abelian Group: Closed, Associative , Identity Element , Inverse, Commutative

1. Let our set be real numbers. Show a binary operator that is not closed
set R (real numbers)
operator : + ---> a + b is always real
operator : - ---> a - b ~ a + (-b) is always real
multiplication : * ---> a * b is always real
divison : / ---> a/b is not real if b=0
so / (divison) is a not closed

operator : Square-root of (a+b)
SR(a+b) is not always real 
example : a = -10 , b = 1, SR(a+b) = SR(-10+1) = SR(-9) = 3i 

2. Find a binary operator that is closed but not associative for real numbers
operator : - ---> a - b != b - a 
- is closed but not associative

3. What algebraic structure (group, monoid, semigroup, etc) is all even integers under addition
set {-5, -3, -1 , 1 , 3, 5, 7}

4. What algebraic structure is all odd integers under multiplication?
{-5, -3, -1 , 1 , 3, 5, 7}

5. Let our set be 3 x 2 matrices of integers under addition. What algebraic structure is this?
Group or Abelian Group
1) closed --> a + b for 3*2 matrix, is always integers matrix
2) Associative --> (a + b) + c = a + (b + c), order doesn't matter 
3) Identity element --> 3 * 2 matrix with all 0 element , A + 0(3 * 2) = A
4) Inverse --> A + (-A) = 0 , for all integers a, there exist -a so that a + (-a) = 0
5) commutative --> a + b = b + a

6. Suppose our set is all rational numbers $\mathbb{Q}$ except $0$ and our binary operator is division. What algebraic structure is this?
1) closed --> a / b is always a rational number
2) Associative --> (a / b) / c != a / (b / c), a = 8, b = 4 , c = 2, so No
3) Identity element --> 1 is identity element, such that a/1 = a but 1/a != a, so No
4) Inverse --> if a != 0, a * (1/a) = 1 (may not be correct without proper identity element)
5) commutative --> a / b != b / a 

This is a Magma

7. Suppose our set is 𓅔 𓆓 **𓆟**
    1. Define a binary operator that makes it a group. You can define the binary operator’s property by constructing a table where the left two columns are the inputs and the right column is the result. Remember you need to allow that the inputs can be the same, for example (𓅔,𓅔) —> ?
    2. Define a binary operator that makes it *not* a group (but it should be closed). Hint: if there is no identity element, then it is not a group

8. What is the size of the smallest possible group? (Remember, a group is a set, so this is asking how large the set is)
1