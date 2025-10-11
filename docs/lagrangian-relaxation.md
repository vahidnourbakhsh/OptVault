This article explains how we can solve a classic transportation problem using Lagrangian relaxation. The purpose of this project is to demonstrate how to decompose a constrained optimization problem into a series of simpler, unconstrained subproblems.

# Overview

This project uses the Lagrangian relaxation technique to find a strong lower bound for the minimum cost of transporting goods from multiple sources to multiple destinations. This method is particularly useful for large-scale optimization problems where standard solvers may struggle due to computational complexity. The core idea is to move the "hard" constraints into the objective function, allowing the problem to be decomposed into smaller, more manageable subproblems. A subgradient optimization approach is then used to iteratively improve the bound.

# Business Problem

The transportation problem is a fundamental challenge in logistics and supply chain management. A company needs to transport goods from a set of warehouses (sources) to a set of retail stores (destinations). Each warehouse has a limited supply of goods, and each store has a specific demand. There is a known cost for shipping one unit of a good from any given warehouse to any given store. The business goal is to determine the optimal shipping plan that satisfies all demand without exceeding any supply, all while minimizing the total transportation cost.

# Mathematical Formulation

Let:
- $m$ be the number of sources (warehouses)
- $n$ be the number of destinations (stores)
- $x_{ij}$ be the quantity of goods shipped from source $i$ to destination $j$
- $c_{ij}$ be the cost of shipping one unit of a good from source $i$ to destination $j$
- $s_{i}$ be the supply available at source $i$
- $d_{j}$ be the demand required at destination $j$

## Objective Function

The objective is to minimize the total transportation cost:

$$\min \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}$$

## Constraints

The solution must satisfy the following constraints:

### Supply Constraints

The total amount of goods shipped from any source $i$ cannot exceed its supply $s_{i}$:

$$\sum_{j=1}^{n}x_{ij} \le s_{i} \quad \forall i=1,\dots,m$$

### Demand Constraints

The total amount of goods received by any destination $j$ must equal its demand $d_{j}$:

$$\sum_{i=1}^{m}x_{ij} = d_{j} \quad \forall j=1,\dots,n$$

### Non-negativity Constraints

The amount of goods shipped must be non-negative:

$$x_{ij} \ge 0 \quad \forall i=1,\dots,m, \forall j=1,\dots,n$$

# Solution Method

## Lagrangian Relaxation

We apply Lagrangian relaxation to solve this problem, specifically by relaxing the demand constraints.

### 1. Form the Lagrangian Subproblem

We move the "hard" demand constraints into the objective function, penalizing their violation with Lagrange multipliers $\lambda_j$. The new objective is:

$$\min \left\{\sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}+\sum_{j=1}^{n}\lambda_j\left(\sum_{i=1}^{m}x_{ij}-d_j\right)\right\}$$

Subject to the remaining (easy) supply and non-negativity constraints.

This expression can be rearranged to reveal its separable structure:

$$\min \left\{\sum_{i=1}^{m}\sum_{j=1}^{n}(c_{ij}+\lambda_j)x_{ij}-\sum_{j=1}^{n}\lambda_j d_j\right\}$$

The minimization can be decomposed into $m$ independent subproblems, one for each source $i$.

### 2. Solve the Subproblem

For a fixed vector of multipliers $\lambda$, each source $i$ solves its own problem:

$$\min \sum_{j=1}^{n}(c_{ij}+\lambda_j)x_{ij}$$

Subject to:

$$\sum_{j=1}^{n}x_{ij} \le s_i$$
$$x_{ij} \ge 0$$

The optimal solution for this simple problem is to ship the entire supply $s_i$ to the single destination $j$ that offers the lowest effective cost $(c_{ij}+\lambda_j)$, provided this minimum cost is non-positive.

### 3. Update the Multipliers with a Subgradient Method

The dual function $L(\lambda)$ is the optimal value of the Lagrangian subproblem for a given $\lambda$. We want to find the $\lambda$ that maximizes this dual function to get the tightest possible lower bound. The dual function is concave but often non-differentiable, so we use a subgradient method.

The subgradient vector $g$ for a given $\lambda^k$ is the vector of demand constraint violations from the optimal subproblem solution $x^k$:

$$g_j^k = \sum_{i=1}^{m}x_{ij}^k - d_j$$

The multipliers are updated iteratively in the direction of the subgradient:

$$\lambda_j^{k+1} = \lambda_j^k + \alpha^k g_j^k$$

where $\alpha^k$ is a decreasing step size.

This process effectively increases the penalty $\lambda_j$ for destinations with excess supply and decreases it for those with unmet demand, pushing the solution towards feasibility.

## 4. Iterate

Steps 2 and 3 are repeated until the multipliers converge, giving a strong lower bound on the optimal solution of the original transportation problem.

# References and Further Reading

Fisher, M. L. (1981). The Lagrangian Relaxation Method for Solving Integer Programming Problems. Management Science, 27(1), 1–18.
Held, M., & Karp, R. M. (1970). The traveling-salesman problem and minimum spanning trees. Operations Research, 18(6), 1138–1162.
Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). Network Flows: Theory, Algorithms, and Applications. Prentice-Hall.
[Lagrangian Relaxation - Wikipedia](https://en.wikipedia.org/wiki/Lagrangian_relaxation)
