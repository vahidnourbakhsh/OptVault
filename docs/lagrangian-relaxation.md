# Lagrangian Relaxation

This document explains how we can solve a classic transportation problem using Lagrangian Relaxation (LR) technique. This is the core insight for deriving the subgradient: For each destination $j$, the $j$-th component of the subgradient is the total amount of goods shipped to that destination minus its required demand.

- If the demand constraint for destination $j$ is met perfectly, the subgradient component $g_j^k$ is zero.
- If destination $j$ has excess supply, $g_j^k > 0$, and the multiplier $\lambda_j$ should be increased (since the dual is being maximized).
- If destination $j$ has an unmet demand, $g_j^k < 0$, and the multiplier $\lambda_j$ should be decreased.

#### Updating the multipliers

In the subgradient method, the multipliers are updated iteratively in the direction of the subgradient. Because we are maximizing the dual function, we take a step in the positive direction of the subgradient. The update rule is:

$$\lambda_j^{k+1} = \lambda_j^k + \alpha^k \cdot g_j^k$$he purpose of this document is to demonstrate how to decompose a constrained optimization problem into a series of simpler, unconstrained subproblems. We also include a python implementation of LR.

## Overview

We use the Lagrangian relaxation technique to find a strong lower bound for the minimum cost of transporting goods from multiple sources to multiple destinations. This method is particularly useful for large-scale optimization problems where standard solvers may struggle due to computational complexity. The core idea is to move the "hard" constraints into the objective function, allowing the problem to be decomposed into smaller, more manageable subproblems. A subgradient optimization approach is then used to iteratively improve the bound.

## Business Problem

The transportation problem is a fundamental challenge in logistics and supply chain management. A company needs to transport goods from a set of warehouses (sources) to a set of retail stores (destinations). Each warehouse has a limited supply of goods, and each store has a specific demand. There is a known cost for shipping one unit of a good from any given warehouse to any given store. The business goal is to determine the optimal shipping plan that satisfies all demand without exceeding any supply, all while minimizing the total transportation cost.

## Mathematical Formulation

Let:

- $m$ be the number of sources (warehouses)
- $n$ be the number of destinations (stores)
- $x_{ij}$ be the quantity of goods shipped from source $i$ to destination $j$
- $c_{ij}$ be the cost of shipping one unit of a good from source $i$ to destination $j$
- $s_{i}$ be the supply available at source $i$
- $d_{j}$ be the demand required at destination $j$

### Objective Function

The objective is to minimize the total transportation cost:

$$\min \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}$$

### Constraints

The solution must satisfy the following constraints:

#### Supply Constraints

The total amount of goods shipped from any source $i$ cannot exceed its supply $s_{i}$:

$$\sum_{j=1}^{n}x_{ij} \le s_{i} \quad \forall i=1,\dots,m$$

#### Demand Constraints

The total amount of goods received by any destination $j$ must equal its demand $d_{j}$:

$$\sum_{i=1}^{m}x_{ij} = d_{j} \quad \forall j=1,\dots,n$$

#### Non-negativity Constraints

The amount of goods shipped must be non-negative:

$$x_{ij} \ge 0 \quad \forall i=1,\dots,m, \forall j=1,\dots,n$$

## Solution Method

### Lagrangian Relaxation

We apply Lagrangian relaxation to solve this problem, specifically by relaxing the demand constraints.

#### 1. Form the Lagrangian Subproblem

We move the "hard" demand constraints into the objective function, penalizing their violation with Lagrange multipliers $\lambda_j$. The new objective is:

$$\min \left\{\sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}+\sum_{j=1}^{n}\lambda_j\left(\sum_{i=1}^{m}x_{ij}-d_j\right)\right\}$$

Subject to the remaining (easy) supply and non-negativity constraints.

This expression can be rearranged to reveal the separable structure of the modified program which makes it easy to solve:

$$\min \left\{\sum_{i=1}^{m}\sum_{j=1}^{n}(c_{ij}+\lambda_j)x_{ij}-\sum_{j=1}^{n}\lambda_j d_j\right\}$$

The minimization can be decomposed into $m$ independent subproblems, one for each source $i$.

#### 2. Solve the Subproblem

For a fixed vector of multipliers $\lambda$, each source $i$ solves its own problem:

$$\min \sum_{j=1}^{n}(c_{ij}+\lambda_j)x_{ij}$$

Subject to:

$$\sum_{j=1}^{n}x_{ij} \le s_i$$
$$x_{ij} \ge 0$$

The optimal solution for this simple problem is to ship the entire supply $s_i$ to the single destination $j$ that offers the lowest effective cost $(c_{ij}+\lambda_j)$, provided this minimum cost is non-positive. When even the lowest effective cost is also positive then optimal solution is to ship zero items: $x_{ij} = 0$.

#### 3. Update the Multipliers with a Subgradient Method

The dual function $L(\lambda)$ is the optimal value of the Lagrangian subproblem for a given $\lambda$. We want to find the $\lambda$ that maximizes this dual function to get the tightest possible lower bound. The dual function is concave but often non-differentiable, so we use a subgradient method.

The subgradient vector $g$ for a given $\lambda^k$ is the vector of demand constraint violations from the optimal subproblem solution $x^k$:

$$g_j^k = \sum_{i=1}^{m}x_{ij}^k - d_j$$

The multipliers are updated iteratively in the direction of the subgradient:

$$\lambda_j^{k+1} = \lambda_j^k + \alpha^k g_j^k$$

where $\alpha^k$ is a decreasing step size.

This process effectively increases the penalty $\lambda_j$ for destinations with excess supply and decreases it for those with unmet demand, pushing the solution towards feasibility.

### 4. Iterate

Steps 2 and 3 are repeated until the multipliers converge, giving a strong lower bound on the optimal solution of the original transportation problem.

## References and Further Reading

Fisher, M. L. (1981). The Lagrangian Relaxation Method for Solving Integer Programming Problems. Management Science, 27(1), 1–18.
Held, M., & Karp, R. M. (1970). The traveling-salesman problem and minimum spanning trees. Operations Research, 18(6), 1138–1162.
Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). Network Flows: Theory, Algorithms, and Applications. Prentice-Hall.
[Lagrangian Relaxation - Wikipedia](https://en.wikipedia.org/wiki/Lagrangian_relaxation)

## Appendix

### Deriving the subgradient for updating Lagrange multipliers

To derive the subgradient for updating Lagrange multipliers, you need to understand the relationship between the Lagrangian dual function and the relaxed constraints. In general, the subgradient of the dual function with respect to a given multiplier is the vector of constraint violations at the optimal solution of the Lagrangian subproblem.

We relax the demand constraints by introducing Lagrange multipliers $\lambda_j$ for each destination $j$. The Lagrangian function is:

$$L(x,\lambda) = \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}+\sum_{j=1}^{n}\lambda_j\left(\sum_{i=1}^{m}x_{ij}-d_j\right)$$

The Lagrangian dual function, denoted as $L(\lambda)$, is the minimum value of the Lagrangian function over the remaining constraints (the supply and non-negativity constraints):

$$L(\lambda) = \min_{x \ge 0, \sum_j x_{ij} \le s_i} L(x,\lambda)$$

The goal of the Lagrangian relaxation algorithm is to find the optimal multipliers $\lambda$ that maximize this dual function:

Maximize $L(\lambda)$

Subject to: $\lambda \in \mathbb{R}^n$ 


#### Deriving the subgradient 

The Lagrangian dual function $L(\lambda)$ is a concave, but often non-differentiable, function. Therefore, we cannot use traditional gradient descent to maximize it. Instead, we use a subgradient method, which generalizes the gradient for non-differentiable functions. A subgradient of a concave function is a vector that defines a hyperplane lying above the function. For our purpose, a subgradient of $L(\lambda)$ at a point $\lambda^k$ is given by the constraint violation at the optimal solution of the Lagrangian subproblem solved with $\lambda^k$. Let $x^k$ be an optimal solution to the Lagrangian subproblem for a given $\lambda^k$:

$$x^k \in \arg \min_{x \ge 0, \sum_j x_{ij} \le s_i} L(x,\lambda^k)$$

The subgradient vector, denoted $g^k$, has components $g_j^k$ for each Lagrange multiplier $\lambda_j$. The component $g_j^k$ is simply the value of the relaxed constraint at the solution $x^k$:

$$g_j^k = \sum_{i=1}^{m}x_{ij}^k - d_j$$

This is the core insight for deriving the subgradient: For each destination $j$, the $j$-th component of the subgradient is the total amount of goods shipped to that destination minus its required demand.If the demand constraint for destination $j$ is met perfectly, the subgradient component $g_{j}^{k}$ is zero.

If destination $j$ has excess supply, $g_{j}^{k}>0$, and the multiplier $\lambda _{j}$ should be increased (since the dual is being maximized).If destination $j$ has an unmet demand, $g_{j}^{k}<0$, and the multiplier $\lambda _{j}$ should be decreased. Updating the multipliers In the subgradient method, the multipliers are updated iteratively in the direction of the subgradient. Because we are maximizing the dual function, we take a step in the positive direction of the subgradient. The update rule is:

$\lambda _{j}^{k+1}=\lambda _{j}^{k}+\alpha ^{k}\cdot g_{j}^{k}$

Where: 

$\lambda _{j}^{k+1}$ is the new value of the multiplier for destination $j$.$\lambda _{j}^{k}$ is the current value. $\alpha ^{k}$ is the step size at iteration $k$. $g_{j}^{k}$ is the subgradient component for destination $j$. Since the multipliers for inequality constraints must be non-negative, the update may be projected onto the non-negative orthant (i.e., we take $\max (0,\lambda _{j}^{k+1})$). The step size $\alpha ^{k}$ is critical for convergence. A common strategy, as used in the Python example, is a decreasing step size, for example, $\alpha ^{k}=\alpha ^{0}/k$. 

#### Example walk-through

Let's trace one iteration of the subgradient calculation for our transportation problem: 

**Assume current multipliers:** We have a vector of Lagrange multipliers $\lambda = [\lambda_1, \lambda_2, \dots, \lambda_n].$

**Solve the subproblem:** The Lagrangian subproblem is solved, which involves each source shipping its supply to the destination with the minimum effective cost. This gives us the flow matrix $x$.

- Let's say source 1 ships its full supply of 100 units to destination 2.
- Source 2 ships its full supply of 150 units to destination 1.
- Source 3 ships its full supply of 200 units to destination 3.

**Check demand fulfillment:** We sum the flows to each destination to see how much demand was satisfied.

- Total shipped to dest 1: $\sum _{i}x_{i1}=0+150+0=150$.

- Total shipped to dest 2: $\sum _{i}x_{i2}=100+0+0=100$.

- Total shipped to dest 3: $\sum _{i}x_{i3}=0+0+200=200$.

**Calculate subgradient:** We compare the total shipped to each destination against the demand d. Let's say the demand vector is d = [100, 150, 250].

- Subgradient component for dest 1: $g_1 = 150 - 100 = 50$ (Excess supply)
- Subgradient component for dest 2: $g_2 = 100 - 150 = -50$ (Unmet demand)
- Subgradient component for dest 3: $g_3 = 200 - 250 = -50$ (Unmet demand)

**Update multipliers:** With a step size $\alpha^k$, we update the multipliers.

- $\lambda_1^{k+1} = \lambda_1^k + \alpha^k \cdot 50$ (Increase penalty for excess supply)
- $\lambda_2^{k+1} = \lambda_2^k + \alpha^k \cdot (-50)$ (Decrease penalty for unmet demand)
- $\lambda_3^{k+1} = \lambda_3^k + \alpha^k \cdot (-50)$ (Decrease penalty for unmet demand) 

This process pushes the algorithm toward a state where the penalties for violating the demand constraints are in balance, which, if the Lagrangian dual has a small duality gap, leads to a near-optimal solution for the original problem.
