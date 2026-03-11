# Homework 2

**Algebraic structures (reminder):**

- **Magma:** Closed
- **Semigroup:** Closed, Associative
- **Monoid:** Closed, Associative, Identity element (e)
- **Group:** Closed, Associative, Identity element, Inverse
- **Abelian group:** Closed, Associative, Identity element, Inverse, Commutative

---

1. **Let our set be the real numbers. Show a binary operator that is not closed.**

   Set: ℝ (real numbers).

   - +, −, × are closed (results always real).
   - **Division (/):** a/b is not in ℝ when b = 0 ⇒ not closed.
   - **Square root of sum:** e.g. √(a+b). For a = −10, b = 1, √(a+b) = √(−9) = 3i ∉ ℝ ⇒ not closed.

2. **Find a binary operator that is closed but not associative on the reals.**

   **Subtraction (−):** a − b is always real (closed). But (a − b) − c ≠ a − (b − c) in general (e.g. (10−5)−2 = 3, 10−(5−2) = 7). So − is closed but not associative.

3. **What algebraic structure is the set of all even integers under addition?**  
   e.g. {…, −4, −2, 0, 2, 4, …}

   **Abelian group:** closed, associative, identity 0, inverse −a, commutative.

4. **What algebraic structure is the set of all odd integers under multiplication?**  
   e.g. {…, −5, −3, −1, 1, 3, 5, …}

   Not closed: odd × odd = odd ✓, but e.g. identity would need to be 1, and 1 is in the set. Inverse: e.g. 1/3 is not an integer ⇒ not a group. It is a **monoid** (closed, associative, identity 1) if we consider only multiplication; no inverse for elements other than ±1.

5. **Let the set be 3×2 matrices of integers under addition. What algebraic structure is this?**

   **Abelian group.**

   - Closed: sum of 3×2 integer matrices is 3×2 integer matrix.
   - Associative: (A+B)+C = A+(B+C).
   - Identity: 3×2 zero matrix.
   - Inverse: A + (−A) = 0 (entries integers).
   - Commutative: A + B = B + A.

6. **Set = ℚ \ {0}, binary operator = division. What algebraic structure?**

   - Closed: a/b ∈ ℚ when a,b ∈ ℚ, b ≠ 0.
   - Not associative: (8/4)/2 = 1, 8/(4/2) = 4.
   - No single identity: a/1 = a but 1/a ≠ a in general.
   - Not commutative: a/b ≠ b/a in general.

   So it is a **magma** (closed) but not a group.

7. **Suppose our set is 𓅔, 𓆓, 𓆟.**

   1. Define a binary operator that makes it a group (e.g. via a Cayley table with rows/columns for 𓅔, 𓆓, 𓆟; each row/column must contain each element exactly once; one element is identity).
   2. Define a binary operator that is closed but not a group (e.g. no identity, or no inverses).

8. **What is the size of the smallest possible group?**

   **1.** The set {e} with e·e = e is a group (trivial group).
