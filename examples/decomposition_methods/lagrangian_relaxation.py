import numpy as np


def solve_lagrangian_relaxation(costs, supply, demand, max_iter=1000, tolerance=1e-5):
    """
    Solves a transportation problem using Lagrangian relaxation.

    Args:
        costs (np.array): Matrix of transportation costs c_ij.
        supply (np.array): Vector of source supplies s_i.
        demand (np.array): Vector of destination demands d_j.
        max_iter (int): Maximum number of subgradient iterations.
        tolerance (float): Stopping tolerance for the subgradient norm.

    Returns:
        tuple: A tuple containing:
            - x (np.array): The optimal flow matrix found by the relaxation.
            - lower_bound (float): The final lower bound on the optimal cost.
    """
    num_sources, num_destinations = costs.shape

    # Initialize Lagrange multipliers and step size parameters
    lambdas = np.zeros(num_destinations)
    step_size_scaling = 1
    best_lower_bound = -np.inf

    for k in range(max_iter):
        # --- Step 1: Solve the Lagrangian subproblem ---
        # The relaxed objective is to minimize sum( (c_ij + lambda_j) * x_ij )
        # subject to supply constraints. This decouples by source.
        x = np.zeros((num_sources, num_destinations))
        total_cost_relaxed = 0.0

        for i in range(num_sources):
            # Find the destination with the minimum effective cost (c_ij + lambda_j)
            effective_costs = costs[i, :] + lambdas

            # Identify the best destination for source i
            best_dest_j = np.argmin(effective_costs)

            # Only ship if the minimum effective cost is negative (profit)
            if effective_costs[best_dest_j] < 0:
                # Ship the entire supply from source i to the best destination
                x[i, best_dest_j] = supply[i]

            # Add cost to the relaxed objective function
            total_cost_relaxed += effective_costs[best_dest_j] * x[i, best_dest_j]

        # Adjust the relaxed objective value by subtracting the penalty term
        lagrangian_lower_bound = total_cost_relaxed - np.sum(lambdas * demand)

        # Update the best lower bound found so far
        best_lower_bound = max(best_lower_bound, lagrangian_lower_bound)

        # --- Step 2: Calculate the subgradient and update multipliers ---
        # The subgradient is the violation of the demand constraints
        subgradient = np.sum(x, axis=0) - demand

        # Calculate the norm of the subgradient
        subgradient_norm = np.linalg.norm(subgradient)
        if subgradient_norm < tolerance:
            print(f"Converged after {k} iterations.")
            break

        # Update the step size
        step_size = step_size_scaling / (k + 1)

        # Update the Lagrange multipliers
        lambdas += step_size * subgradient

        if k % 100 == 0:
            print(
                f"Iteration {k}: Lower Bound = {lagrangian_lower_bound:.4f}, Subgradient Norm = {subgradient_norm:.4f}"
            )

    return x, best_lower_bound


# --- Example usage ---
if __name__ == "__main__":
    # Define problem data
    costs = np.array([[10, 2, 8], [4, 7, 5], [9, 6, 3]])
    supply = np.array([50, 60, 40])
    demand = np.array([30, 70, 50])

    # Solve using Lagrangian relaxation
    x_solution, lower_bound = solve_lagrangian_relaxation(
        costs, supply, demand, max_iter=int(10e6), tolerance=1e-4
    )

    print("\n--- Results ---")
    print(f"Final Lower Bound: {lower_bound:.4f}")
    print("\nApproximate Transportation Plan (x_ij):")
    print(np.round(x_solution, 2))
    print("\nDemand satisfaction based on relaxation:")
    print(np.sum(x_solution, axis=0))
    print("Demand required:")
    print(demand)

    # Note on solution feasibility:
    # The final solution `x_solution` is not guaranteed to be feasible
    # for the original problem. The strength of Lagrangian relaxation is
    # in providing a good lower bound and potentially a feasible solution
    # through a heuristic. A follow-up step would be required to adjust
    # `x_solution` to satisfy the constraints while staying close to the
    # bound.
