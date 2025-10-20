# Lagrangian Relaxation

This document explains how we can solve a classic transportation problem using Lagrangian Relaxation (LR) technique. The purpose of the LR technique is to decompose a constrained optimization problem into a series of simpler, unconstrained subproblems.

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

$$\min \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}+\sum_{j=1}^{n}\lambda_j\left(\sum_{i=1}^{m}x_{ij}-d_j\right)$$

Subject to the remaining (easy) supply and non-negativity constraints.

This expression can be rearranged to reveal the separable structure of the modified program which makes it easy to solve:

$$\min \sum_{i=1}^{m}\sum_{j=1}^{n}(c_{ij}+\lambda_j)x_{ij}-\sum_{j=1}^{n}\lambda_j d_j$$

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

- Fisher, M. L. (1981). The Lagrangian Relaxation Method for Solving Integer Programming Problems. *Management Science*, 27(1), 1–18.
- Held, M., & Karp, R. M. (1970). The traveling-salesman problem and minimum spanning trees. *Operations Research*, 18(6), 1138–1162.
- Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). *Network Flows: Theory, Algorithms, and Applications*. Prentice-Hall.
- [Lagrangian Relaxation - Wikipedia](https://en.wikipedia.org/wiki/Lagrangian_relaxation)

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

The Lagrangian dual function $L(\lambda)$ is a concave, but often non-differentiable, function. Therefore, we cannot use traditional gradient descent to maximize it. Instead, we use a subgradient method, which generalizes the gradient for non-differentiable functions. A subgradient of a concave function is a vector that defines a hyperplane lying above the function. For our purpose, a subgradient of $L(\lambda)$ at a point $\lambda^k$ is given by the constraint violation at the optimal solution of the Lagrangian subproblem solved with $\lambda^k$. Let $x^k$ be an optimal solution to the Lagrangian subproblem for a given $\lambda^k$:

$$x^k \in \arg \min_{x \ge 0, \sum_j x_{ij} \le s_i} L(x,\lambda^k)$$

The subgradient vector, denoted $g^k$, has components $g_j^k$ for each Lagrange multiplier $\lambda_j$. The component $g_j^k$ is simply the value of the relaxed constraint at the solution $x^k$:

$$g_j^k = \sum_{i=1}^{m}x_{ij}^k - d_j$$

This is the core insight for deriving the subgradient: For each destination $j$, the $j$-th component of the subgradient is the total amount of goods shipped to that destination minus its required demand. If the demand constraint for destination $j$ is met perfectly, the subgradient component $g_{j}^{k}$ is zero.

If destination $j$ has excess supply, $g_{j}^{k}>0$, and the multiplier $\lambda_{j}$ should be increased (since the dual is being maximized). If destination $j$ has an unmet demand, $g_{j}^{k}<0$, and the multiplier $\lambda_{j}$ should be decreased.

#### Updating the multipliers

In the subgradient method, the multipliers are updated iteratively in the direction of the subgradient. Because we are maximizing the dual function, we take a step in the positive direction of the subgradient. The update rule is:

$$\lambda_{j}^{k+1}=\lambda_{j}^{k}+\alpha^{k} \cdot g_{j}^{k}$$

Where:

- $\lambda_{j}^{k+1}$ is the new value of the multiplier for destination $j$.
- $\lambda_{j}^{k}$ is the current value.
- $\alpha^{k}$ is the step size at iteration $k$.
- $g_{j}^{k}$ is the subgradient component for destination $j$.

Since the multipliers for inequality constraints must be non-negative, the update may be projected onto the non-negative orthant (i.e., we take $\max(0, \lambda_{j}^{k+1})$). The step size $\alpha^{k}$ is critical for convergence. A common strategy, as used in the Python example, is a decreasing step size, for example, $\alpha^{k}=\alpha^{0}/k$.

#### Example walk-through

Let's trace one iteration of the subgradient calculation for our transportation problem:

**Assume current multipliers:** We have a vector of Lagrange multipliers $\lambda = [\lambda_1, \lambda_2, \dots, \lambda_n]$.

**Solve the subproblem:** The Lagrangian subproblem is solved, which involves each source shipping its supply to the destination with the minimum effective cost. This gives us the flow matrix $x$.

- Let's say source 1 ships its full supply of 100 units to destination 2.
- Source 2 ships its full supply of 150 units to destination 1.
- Source 3 ships its full supply of 200 units to destination 3.

**Check demand fulfillment:** We sum the flows to each destination to see how much demand was satisfied.

- Total shipped to dest 1: $\sum_{i}x_{i1}=0+150+0=150$.
- Total shipped to dest 2: $\sum_{i}x_{i2}=100+0+0=100$.
- Total shipped to dest 3: $\sum_{i}x_{i3}=0+0+200=200$.

**Calculate subgradient:** We compare the total shipped to each destination against the demand $d$. Let's say the demand vector is $d = [100, 150, 250]$.

- Subgradient component for dest 1: $g_1 = 150 - 100 = 50$ (Excess supply)
- Subgradient component for dest 2: $g_2 = 100 - 150 = -50$ (Unmet demand)
- Subgradient component for dest 3: $g_3 = 200 - 250 = -50$ (Unmet demand)

**Update multipliers:** With a step size $\alpha^k$, we update the multipliers.

- $\lambda_1^{k+1} = \lambda_1^k + \alpha^k \cdot 50$ (Increase penalty for excess supply)
- $\lambda_2^{k+1} = \lambda_2^k + \alpha^k \cdot (-50)$ (Decrease penalty for unmet demand)
- $\lambda_3^{k+1} = \lambda_3^k + \alpha^k \cdot (-50)$ (Decrease penalty for unmet demand)

This process pushes the algorithm toward a state where the penalties for violating the demand constraints are in balance, which, if the Lagrangian dual has a small duality gap, leads to a near-optimal solution for the original problem.

#### Example walk-through 2

**Original problem:**

Minimize $\sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}$

Subject to:

- Supply constraints: $\sum_{j=1}^{n}x_{ij} \le s_i$
- Demand constraints: $\sum_{i=1}^{m}x_{ij} = d_j$
- Non-negativity: $x_{ij} \ge 0$

**Example Data:**

Let's assume there are 2 sources and 3 destinations.

Costs $(c_{ij})$:

$$C = \begin{pmatrix}
10 & 8 & 5 \\
6 & 12 & 9
\end{pmatrix}$$

Supply $(s_i)$:

$$s = \begin{pmatrix}
100 \\
120
\end{pmatrix}$$

Demand $(d_j)$:

$$d = \begin{pmatrix}
60 \\
80 \\
80
\end{pmatrix}$$

Total supply = 220, total demand = 220.

### Step-by-step Lagrangian Relaxation

**Initial state (Iteration 0):**

- Initialize Lagrange multipliers $\lambda_j = 0$ for all $j$.
- Let's use a step size scaling factor of $\alpha^0 = 1$.
- Best lower bound found so far: $L^* = -\infty$.

**Iteration 1:**

1. **Solve the Lagrangian subproblem**

    The relaxed objective is to minimize:
    $$\sum_{i=1}^{2}\sum_{j=1}^{3}(c_{ij}+\lambda_j)x_{ij} - \sum_{j=1}^{3}\lambda_j d_j$$

    Since all $\lambda_j$ are 0, the effective costs $(c_{ij}+\lambda_j)$ are just the original costs.

    - **Source 1:** Supply $s_1 = 100$. Effective costs are $(10, 8, 5)$. The minimum is 5 at destination 3. Source 1 ships its entire supply to destination 3: $x_{11} = 0, x_{12} = 0, x_{13} = 100$.
    - **Source 2:** Supply $s_2 = 120$. Effective costs are $(6, 12, 9)$. The minimum is 6 at destination 1. Source 2 ships its entire supply to destination 1: $x_{21} = 120, x_{22} = 0, x_{23} = 0$.

    The solution matrix $x$ for this iteration is:

    $$x = \begin{pmatrix}
    0 & 0 & 100 \\
    120 & 0 & 0
    \end{pmatrix}$$

2. **Calculate the dual objective (lower bound)**

    The dual objective value $L(\lambda^1)$ is calculated using the subproblem solution $x^1$ and the current multipliers $\lambda^1$:
    $$L(\lambda^1) = \sum_{i,j}c_{ij}x_{ij}^1 + \sum_j\lambda_j\left(\sum_i x_{ij}^1 - d_j\right)$$

    Since $\lambda_j = 0$, this simplifies to the cost of the current solution:
    $$L(\lambda^1) = (10 \cdot 0) + (8 \cdot 0) + (5 \cdot 100) + (6 \cdot 120) + (12 \cdot 0) + (9 \cdot 0) = 500 + 720 = 1220$$

    $L^* = \max(-\infty, 1220) = 1220$

3. **Calculate the subgradient and update multipliers**

    The subgradient $g$ is the vector of demand constraint violations:
    - $g_1 = \sum_i x_{i1} - d_1 = (0 + 120) - 60 = 60$ (Excess supply)
    - $g_2 = \sum_i x_{i2} - d_2 = (0 + 0) - 80 = -80$ (Unmet demand)
    - $g_3 = \sum_i x_{i3} - d_3 = (100 + 0) - 80 = 20$ (Excess supply)

    The subgradient vector is $g = (60, -80, 20)$.

    Update the multipliers using a step size $\alpha^1 = \alpha^0/1 = 1$:
    - $\lambda_1^2 = \lambda_1^1 + \alpha^1 g_1^1 = 0 + 1 \cdot 60 = 60$
    - $\lambda_2^2 = \lambda_2^1 + \alpha^1 g_2^1 = 0 + 1 \cdot (-80) = -80$
    - $\lambda_3^2 = \lambda_3^1 + \alpha^1 g_3^1 = 0 + 1 \cdot 20 = 20$

    The new multipliers are $\lambda^2 = (60, -80, 20)$.

**Iteration 2:**

1. **Solve the Lagrangian subproblem**

    New effective costs are $c_{ij} + \lambda_j^2$:

    $$C_{eff} = \begin{pmatrix}
    10+60 & 8-80 & 5+20 \\
    6+60 & 12-80 & 9+20
    \end{pmatrix} = \begin{pmatrix}
    70 & -72 & 25 \\
    66 & -68 & 29
    \end{pmatrix}$$

    - **Source 1:** Supply $s_1 = 100$. Effective costs are $(70, -72, 25)$. The minimum is -72 at destination 2. Source 1 ships its entire supply to destination 2: $x_{11} = 0, x_{12} = 100, x_{13} = 0$.
    - **Source 2:** Supply $s_2 = 120$. Effective costs are $(66, -68, 29)$. The minimum is -68 at destination 2. Source 2 ships its entire supply to destination 2: $x_{21} = 0, x_{22} = 120, x_{23} = 0$.

    The solution matrix $x$ for this iteration is:

    $$x = \begin{pmatrix}
    0 & 100 & 0 \\
    0 & 120 & 0
    \end{pmatrix}$$

2. **Calculate the dual objective (lower bound)**

    $$L(\lambda^2) = \sum_{i,j}c_{ij}x_{ij}^2 + \sum_j\lambda_j^2\left(\sum_i x_{ij}^2 - d_j\right)$$
    $$L(\lambda^2) = [(10 \cdot 0) + (8 \cdot 100) + (5 \cdot 0) + (6 \cdot 0) + (12 \cdot 120) + (9 \cdot 0)] + [60(0-60) + (-80)(220-80) + 20(0-80)]$$
    $$L(\lambda^2) = (800 + 1440) + [(-3600) + (-11200) + (-1600)] = 2240 - 16400 = -14160$$

    Wait, this is an obvious error in the example. The Lagrangian dual function is maximized, and it must produce a valid lower bound. Let's recheck the formula. The Lagrangian dual is defined as $L(\lambda) = \min_{x \in X}\{cx + \lambda(Ax - b)\}$. A better calculation is to calculate the minimum value of the relaxed objective directly:

    $$L(\lambda^2) = (70 \cdot 0) + (-72 \cdot 100) + (25 \cdot 0) + (66 \cdot 0) + (-68 \cdot 120) + (29 \cdot 0) - \sum \lambda_j d_j$$
    $$L(\lambda^2) = -7200 - 8160 - [(60 \cdot 60) + (-80 \cdot 80) + (20 \cdot 80)]$$
    $$L(\lambda^2) = -15360 - [3600 - 6400 + 1600] = -15360 - (-1200) = -14160$$

    The calculation was correct. The dual objective can indeed decrease. $L^* = \max(1220, -14160) = 1220$.

3. **Calculate the subgradient and update multipliers**

    - $g_1 = \sum_i x_{i1} - d_1 = (0 + 0) - 60 = -60$
    - $g_2 = \sum_i x_{i2} - d_2 = (100 + 120) - 80 = 140$
    - $g_3 = \sum_i x_{i3} - d_3 = (0 + 0) - 80 = -80$

    The subgradient vector is $g = (-60, 140, -80)$.

    Update multipliers with a smaller step size, say $\alpha^2 = \alpha^0/2 = 0.5$:
    - $\lambda_1^3 = \lambda_1^2 + \alpha^2 g_1^2 = 60 + 0.5 \cdot (-60) = 30$
    - $\lambda_2^3 = \lambda_2^2 + \alpha^2 g_2^2 = -80 + 0.5 \cdot 140 = -10$
    - $\lambda_3^3 = \lambda_3^2 + \alpha^2 g_3^2 = 20 + 0.5 \cdot (-80) = -20$

    The new multipliers are $\lambda^3 = (30, -10, -20)$.

**Iteration 3:**

1. **Solve the Lagrangian subproblem**

    Effective costs are $c_{ij} + \lambda_j^3$:

    $$C_{eff} = \begin{pmatrix}
    10+30 & 8-10 & 5-20 \\
    6+30 & 12-10 & 9-20
    \end{pmatrix} = \begin{pmatrix}
    40 & -2 & -15 \\
    36 & 2 & -11
    \end{pmatrix}$$

    - **Source 1:** Supply $s_1 = 100$. Minimum cost is -15 at dest 3: $x_{11} = 0, x_{12} = 0, x_{13} = 100$.
    - **Source 2:** Supply $s_2 = 120$. Minimum cost is -11 at dest 3: $x_{21} = 0, x_{22} = 0, x_{23} = 120$.

    The solution matrix $x$ for this iteration is:

    $$x = \begin{pmatrix}
    0 & 0 & 100 \\
    0 & 0 & 120
    \end{pmatrix}$$

2. **Calculate the dual objective**

    $$L(\lambda^3) = -15 \cdot 100 - 11 \cdot 120 - [(30 \cdot 60) + (-10 \cdot 80) + (-20 \cdot 80)]$$
    $$L(\lambda^3) = -1500 - 1320 - [1800 - 800 - 1600] = -2820 - (-600) = -2220$$

    $L^* = \max(1220, -2220) = 1220$

3. **Calculate the subgradient and update multipliers**

    - $g_1 = (0 + 0) - 60 = -60$
    - $g_2 = (0 + 0) - 80 = -80$
    - $g_3 = (100 + 120) - 80 = 140$

    The subgradient vector is $g = (-60, -80, 140)$.

The process continues, with the lower bound $L^*$ being tracked and the multipliers adjusted. The subgradient method helps explore the space of multipliers, improving the lower bound and pushing the solution towards satisfying the relaxed constraints.

This example illustrates:

- The iterative nature of the process
- How the subproblem solution depends on the multipliers
- How the subgradient, which represents the constraint violation, guides the update of the multipliers
- The fact that the primal solution ($x$) is not necessarily feasible during the intermediate steps

### Connection between the subgradient and the dual function

The subgradient of the dual function is directly derived from the solution to the Lagrangian subproblem. For the transportation problem, this connection can be explained through two complementary perspectives: the formal mathematical definition and a more intuitive economic interpretation.

#### Formal mathematical connection

**The dual function $L(\lambda)$:** In Lagrangian relaxation, we form the dual function $L(\lambda)$ by minimizing the Lagrangian over the "easy" constraints. For our transportation example, with demand constraints relaxed:

$$L(\lambda)=\min_{x\ge 0,\sum _{j}x_{ij}\le s_{i}} \sum _{i,j}c_{ij}x_{ij}+\sum _{j}\lambda _{j}\left(\sum _{i}x_{ij}-d_{j}\right)$$

**The subgradient definition:** For a concave function like $L(\lambda)$, a subgradient $g$ at a point $\lambda$ is any vector that satisfies the inequality:

$$L(\bar{\lambda}) \leq L(\lambda) + g^T(\bar{\lambda} - \lambda) \text{ for all } \bar{\lambda}$$

This means the affine function $L(\lambda) + g^T(\bar{\lambda} - \lambda)$ lies above the function $L(\bar{\lambda})$.

**The key result:** It can be proven that the subgradient vector $g$ of the dual function $L(\lambda)$ at a point $\lambda^k$ is given by the vector of constraint violations at the optimal solution $x^k$ of the Lagrangian subproblem for $\lambda^k$.

Let $x^k$ be an optimal solution to the Lagrangian subproblem for a given $\lambda^k$.

The dual function can be written as $L(\lambda) = \min_{x \in X}(c^T x + \lambda^T(Ax - b))$.

The subgradient is then derived from the terms related to $\lambda$: $\nabla_{\lambda} L(\lambda) = Ax - b$.

For our specific transportation problem, the constraint is $\sum_i x_{ij} = d_j$. The $j$-th component of the subgradient is:

$$g_j^k = \sum_{i=1}^m x_{ij}^k - d_j$$

#### Intuitive economic interpretation

The subgradient provides a powerful economic interpretation of the dual variables, or shadow prices, that guide the optimization process.

**Lagrange multipliers as prices:** In the context of the transportation problem, the Lagrange multipliers $\lambda_{j}$ can be thought of as prices or tolls associated with the demand constraints at each destination $j$.

**The subproblem response:** When the multipliers are set, each source independently solves its own subproblem. It is trying to maximize its profit or minimize its cost given the costs $c_{ij}$ and the "prices" $\lambda_{j}$ for shipping to each destination.

**Subgradient as excess demand/supply:** The subgradient vector $g_{j}^{k}$ measures the difference between the total amount of goods shipped to destination $j$ and its demand.

- If $g_{j}^{k}>0$ (excess supply), it means the current price $\lambda_{j}$ is too high, attracting more goods than needed. The subgradient update $\lambda_{j}^{k+1}=\lambda_{j}^{k}+\alpha^{k}g_{j}^{k}$ will increase the price, effectively discouraging sources from shipping to that destination in the next iteration.
- If $g_{j}^{k}<0$ (unmet demand), the current price $\lambda_{j}$ is too low. The update will decrease the penalty (or make the "reward" more attractive), encouraging sources to ship more goods to that destination.

**Toward equilibrium:** The subgradient method uses this feedback loop to adjust the prices (multipliers) toward a state of market equilibrium where supply meets demand. When the subgradient is close to zero, it signifies that the demands are being met and the dual solution is stabilizing.

#### Practical benefits of this connection

**Decomposition:**
The core of Lagrangian relaxation is that the subgradient calculation can be decomposed. Each subproblem (for each source in our example) can be solved independently, and their results are "gathered" to form the full subgradient. This allows for efficient parallel computation for large-scale problems.

**Guidance for the primal problem:** Even though the primal solution $x^{k}$ from the subproblem may not be feasible for the original problem, the dual information derived from the subgradient guides the search for better feasible solutions. A good dual solution with an acceptable duality gap implies the optimal primal solution is not far away.

**Handling non-differentiability:** The ability to use a subgradient rather than a gradient is crucial for problems where the dual function is non-differentiable. This occurs at points where multiple solutions to the subproblem exist. The subgradient method naturally handles these "kinks" in the dual function, unlike standard gradient ascent methods.
