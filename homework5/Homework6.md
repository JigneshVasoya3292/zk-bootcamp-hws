# Homework 6

Implement a Solidity contract (or Python code if you don't want to use Solidity) that verifies the computation for the EC points.

$$
0 = -A_1 B_2 + \alpha_1 \beta_2 + X_1 \gamma_2 + C_1 \delta_2
$$

with

$$
X_1 = x_1 G_1 + x_2 G_1 + x_3 G_1
$$

Pick any (nontrivial) values to generate the points that result in a balanced equation.

**Constraints:**

- x₁, x₂, x₃ are `uint256`; the rest are G1 or G2 points.
- The contract must take as arguments to a public function: **A₁, B₂, C₁, x₁, x₂, x₃**.
- Use Ethereum precompiles for EC addition and scalar multiplication to compute X₁, then the pairing precompile to evaluate the equation in one go.
- All other points (α₁, β₂, γ₂, δ₂, etc.) must be hardcoded as constants in the contract. For example, if α₁ = 5·G₁, β₂ = 6·G₂, etc., compute those values offline and write them as constants in the contract.

**Tip:** Get the pairing working with only two pairs (e.g. 2 G1 points and 2 G2 points) first with simple examples. The order for G2 in the precompile is not what you might expect.
