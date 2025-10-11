import numpy as np


def solve_lagrangian_relaxation(costs, supply, demand, max_iter=1000, tolerance=1e-5):
    """
    Solves a transportation problem using Lagrangian relaxation and a subgradient method.

    This method relaxes the demand constraints and iteratively updates Lagrange multipliers
    to find a tight lower bound for the original problem.

    Args:
        costs (np.array): Matrix of transportation costs c_ij.
        supply (np.array): Vector of source supplies s_i.
        demand (np.array): Vector of destination demands d_j.
        max_iter (int): Maximum number of subgradient iterations.
        tolerance (float): Stopping tolerance for the subgradient norm.

    Returns:
        tuple: A tuple containing:
            - x (np.array): The optimal flow matrix from the final subproblem.
            - best_lower_bound (float): The best lower bound found.
    """
    num_sources, num_destinations = costs.shape

    # Initialize Lagrange multipliers (λ) for demand constraints.
    lambdas = np.zeros(num_destinations)

    # Step size parameters for the subgradient method.
    step_size_scaling = 1.0
    best_lower_bound = -np.inf

    print("Starting Lagrangian Relaxation...")

    for k in range(max_iter):
        # --- 1. Solve the Lagrangian subproblem ---
        # The relaxed objective is to minimize sum( (c_ij + lambda_j) * x_ij )
        # subject to supply constraints. This decouples by source.
        x = np.zeros((num_sources, num_destinations))
        total_cost_relaxed = 0.0

        # For each source, find the destination with the minimum effective cost.
        for i in range(num_sources):
            # Effective cost includes the original cost plus the penalty from lambdas.
            effective_costs = costs[i, :] + lambdas

            # Identify the best destination for source i.
            best_dest_j = np.argmin(effective_costs)

            # If the minimum effective cost is non-positive, ship the entire supply.
            if effective_costs[best_dest_j] < 0:
                x[i, best_dest_j] = supply[i]

            # Add cost to the relaxed objective function.
            total_cost_relaxed += effective_costs[best_dest_j] * x[i, best_dest_j]

        # Calculate the lower bound on the optimal cost of the original problem.
        # This is the dual objective value.
        lagrangian_lower_bound = total_cost_relaxed - np.sum(lambdas * demand)

        # Update the best lower bound found so far.
        best_lower_bound = max(best_lower_bound, lagrangian_lower_bound)

        # --- 2. Calculate the subgradient ---
        # The subgradient is the violation of the demand constraints.
        subgradient = np.sum(x, axis=0) - demand

        # Calculate the norm of the subgradient for convergence check.
        subgradient_norm = np.linalg.norm(subgradient)

        if subgradient_norm < tolerance:
            print(f"Converged after {k} iterations.")
            break

        # --- 3. Update the Lagrange multipliers ---
        # The step size is typically decreased over iterations.
        step_size = step_size_scaling / (k + 1)

        # Update the Lagrange multipliers in the direction of the subgradient.
        lambdas += step_size * subgradient

        if k % 100 == 0:
            print(
                f"Iteration {k}: Lower Bound = {lagrangian_lower_bound:.4f}, Subgradient Norm = {subgradient_norm:.4f}"
            )

    # Ensure non-negative multipliers if appropriate (can be negative for equality constraints).
    lambdas = np.maximum(lambdas, 0)

    print("\n--- Lagrangian Relaxation Complete ---")

    return x, best_lower_bound


# --- Example usage ---
if __name__ == "__main__":
    # Define problem data (costs, supply, demand)
    costs = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
    supply = np.array([100, 150, 200])
    demand = np.array([120, 130, 200])

    # Solve using Lagrangian relaxation
    x_solution, lower_bound = solve_lagrangian_relaxation(costs, supply, demand)

    print("\n--- Results ---")
    print(f"Final Best Lower Bound: {lower_bound:.4f}")
    print("\nApproximate Transportation Plan (x_ij from final iteration):")
    print(np.round(x_solution, 2))
    print("\nDemand satisfaction based on relaxation:")
    print(np.sum(x_solution, axis=0))
    print("Required demand:")
    print(demand)
