"""Substitution-based inventory optimization models."""

from typing import Dict, List, Optional, Tuple

import pandas as pd
from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

__all__ = ["SubstitutionInventoryOptimizer"]


class SubstitutionInventoryOptimizer:
    """
    Multi-item inventory optimization model with substitutions.

    This model optimizes inventory levels across multiple items while allowing
    for customer substitutions when primary items are out of stock.
    """

    def __init__(
        self,
        items: List[str],
        days: int,
        demand: Dict[str, List[float]],
        substitution_rates: Dict[Tuple[str, str], float],
        costs: Dict[str, float],
        safety_stock: Dict[str, float],
        presentation_stock: Dict[str, float],
        shrink_rates: Dict[str, float],
        order_days: List[int],
        lead_time: int = 1,
        initial_inventory: Optional[Dict[str, float]] = None,
        penalty_cost: float = 100.0,
    ):
        """
        Initialize the substitution inventory optimization model.

        Args:
            items: List of item names
            days: Number of days in planning horizon
            demand: Forecasted demand for each item by day {item: [day0, day1, ...]}
            substitution_rates: Substitution rates {(from_item, to_item): rate}
            costs: Unit costs for each item {item: cost}
            safety_stock: Safety stock levels {item: level}
            presentation_stock: Minimum display stock {item: level}
            shrink_rates: Shrinkage rates per period {item: rate}
            order_days: Binary list indicating order days [1, 0, 1, ...]
            lead_time: Order lead time in days
            initial_inventory: Starting inventory {item: level}, defaults to 50
            penalty_cost: Penalty cost per unit of unmet demand
        """
        self.items = items
        self.days = days
        self.demand = demand
        self.substitution_rates = substitution_rates
        self.costs = costs
        self.safety_stock = safety_stock
        self.presentation_stock = presentation_stock
        self.shrink_rates = shrink_rates
        self.order_days = order_days
        self.lead_time = lead_time
        self.initial_inventory = initial_inventory or {item: 50.0 for item in items}
        self.penalty_cost = penalty_cost

        # Model components
        self.problem = None
        self.variables = {}
        self.results = None

    def build_model(self) -> None:
        """Build the optimization model."""
        # Initialize problem
        self.problem = LpProblem("Substitution_Inventory_Optimization", LpMinimize)

        # Decision variables with clear, descriptive names

        # Order quantities: How much to order for each item at each time period
        self.variables["order_qty"] = {
            (i, t): LpVariable(f"OrderQty_{i}_{t}", lowBound=0)
            for i in self.items
            for t in range(self.days)
        }

        # Inventory levels: Stock on hand for each item at each time period
        self.variables["inventory"] = {
            (i, t): LpVariable(f"Inventory_{i}_{t}", lowBound=0)
            for i in self.items
            for t in range(self.days)
        }

        # Unmet demand: Demand that couldn't be satisfied for each item at each time period
        self.variables["unmet_demand"] = {
            (i, t): LpVariable(f"UnmetDemand_{i}_{t}", lowBound=0)
            for i in self.items
            for t in range(self.days)
        }

        # Substitution flow: Amount of demand for item i satisfied by item j at each time period
        self.variables["substitution_flow"] = {
            (i, j, t): LpVariable(f"SubstFlow_{i}_to_{j}_{t}", lowBound=0)
            for i in self.items
            for j in self.items
            if i != j
            for t in range(self.days)
        }

        # Objective: Minimize ordering cost + penalty for unmet demand
        self.problem += lpSum(
            self.costs[i] * self.variables["order_qty"][i, t]
            for i in self.items
            for t in range(self.days)
        ) + lpSum(
            self.penalty_cost * self.variables["unmet_demand"][i, t]
            for i in self.items
            for t in range(self.days)
        )

        # Constraints
        self._add_inventory_constraints()
        self._add_unmet_demand_constraints()
        self._add_substitution_constraints()
        self._add_minimum_inventory_constraints()
        self._add_ordering_constraints()

    def _add_inventory_constraints(self) -> None:
        """Add inventory balance constraints."""
        for t in range(self.days):
            for i in self.items:
                if t == 0:
                    # Initial period
                    self.problem += self.variables["inventory"][
                        i, t
                    ] == self.initial_inventory[i] - self.demand[i][t] + lpSum(
                        self.variables["substitution_flow"][j, i, t]
                        for j in self.items
                        if j != i
                    ) - lpSum(
                        self.variables["substitution_flow"][i, j, t]
                        for j in self.items
                        if j != i
                    )
                else:
                    # Regular periods
                    arrival = (
                        self.variables["order_qty"][i, t - self.lead_time]
                        if t >= self.lead_time
                        else 0
                    )
                    self.problem += (
                        self.variables["inventory"][i, t]
                        == self.variables["inventory"][i, t - 1]
                        + arrival
                        - self.demand[i][t]
                        + lpSum(
                            self.variables["substitution_flow"][j, i, t]
                            for j in self.items
                            if j != i
                        )
                        - lpSum(
                            self.variables["substitution_flow"][i, j, t]
                            for j in self.items
                            if j != i
                        )
                        - self.shrink_rates[i] * self.variables["inventory"][i, t - 1]
                    )

    def _add_unmet_demand_constraints(self) -> None:
        """Add unmet demand constraints."""
        for t in range(self.days):
            for i in self.items:
                if t == 0:
                    available_inventory = self.initial_inventory[i]
                else:
                    available_inventory = self.variables["inventory"][i, t - 1]

                arrival = (
                    self.variables["order_qty"][i, t - self.lead_time]
                    if t >= self.lead_time
                    else 0
                )

                self.problem += self.variables["unmet_demand"][i, t] >= self.demand[i][
                    t
                ] - available_inventory - arrival - lpSum(
                    self.variables["substitution_flow"][j, i, t]
                    for j in self.items
                    if j != i
                )

    def _add_substitution_constraints(self) -> None:
        """Add substitution limit constraints."""
        for t in range(self.days):
            for i in self.items:
                for j in self.items:
                    if i != j:
                        if (i, j) in self.substitution_rates:
                            # Allow substitution up to the specified rate
                            self.problem += (
                                self.variables["substitution_flow"][i, j, t]
                                <= self.substitution_rates[i, j]
                                * self.variables["unmet_demand"][i, t]
                            )
                        else:
                            # No substitution allowed if rate not specified
                            self.problem += (
                                self.variables["substitution_flow"][i, j, t] == 0
                            )

    def _add_minimum_inventory_constraints(self) -> None:
        """Add minimum inventory constraints."""
        for t in range(self.days):
            for i in self.items:
                self.problem += (
                    self.variables["inventory"][i, t]
                    >= self.safety_stock[i] + self.presentation_stock[i]
                )

    def _add_ordering_constraints(self) -> None:
        """Add ordering day constraints."""
        for t in range(self.days):
            for i in self.items:
                # Big M constraint: can only order on allowed days
                self.problem += (
                    self.variables["order_qty"][i, t] <= 10000 * self.order_days[t]
                )

    def solve(self) -> Dict:
        """
        Solve the optimization model.

        Returns:
            Dictionary with optimization results
        """
        if self.problem is None:
            self.build_model()

        # Solve the problem
        status = self.problem.solve()

        # Extract results
        self.results = {
            "status": LpStatus[status],
            "objective_value": value(self.problem.objective),
            "orders": {},
            "inventory": {},
            "unmet_demand": {},
            "substitutions": {},
        }

        # Extract variable values
        for t in range(self.days):
            for i in self.items:
                self.results["orders"][(i, t)] = value(
                    self.variables["order_qty"][i, t]
                )
                self.results["inventory"][(i, t)] = value(
                    self.variables["inventory"][i, t]
                )
                self.results["unmet_demand"][(i, t)] = value(
                    self.variables["unmet_demand"][i, t]
                )

                for j in self.items:
                    if i != j:
                        sub_value = value(self.variables["substitution_flow"][i, j, t])
                        if sub_value and sub_value > 0:
                            self.results["substitutions"][(i, j, t)] = sub_value

        return self.results

    def print_results(self) -> None:
        """Print a formatted summary of the optimization results."""
        if not self.results:
            print("No results available. Run solve() first.")
            return

        print(f"Optimization Status: {self.results['status']}")
        print(f"Total Cost: {self.results['objective_value']:.2f}")
        print("\nDaily Results:")
        print("-" * 80)

        for t in range(self.days):
            print(f"Day {t}:")
            for i in self.items:
                order = self.results["orders"][(i, t)]
                inventory = self.results["inventory"][(i, t)]
                unmet = self.results["unmet_demand"][(i, t)]
                print(
                    f"  {i}: Order = {order:.1f}, Inventory = {inventory:.1f}, "
                    f"Unmet = {unmet:.1f}"
                )

            # Print substitutions for this day
            day_subs = {
                k: v for k, v in self.results["substitutions"].items() if k[2] == t
            }
            if day_subs:
                for (from_item, to_item, _), amount in day_subs.items():
                    print(f"    Sub {from_item} -> {to_item}: {amount:.1f}")
            print()

    def get_results_dataframe(self) -> pd.DataFrame:
        """
        Return results as a pandas DataFrame for easy analysis.

        Returns:
            DataFrame with columns: day, item, order, inventory, unmet_demand
        """
        if not self.results:
            raise ValueError("No results available. Run solve() first.")

        data = []
        for t in range(self.days):
            for i in self.items:
                data.append(
                    {
                        "day": t,
                        "item": i,
                        "order": self.results["orders"][(i, t)],
                        "inventory": self.results["inventory"][(i, t)],
                        "unmet_demand": self.results["unmet_demand"][(i, t)],
                        "demand": self.demand[i][t],
                    }
                )

        return pd.DataFrame(data)

    def get_variable_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all decision variables.

        Returns:
            Dictionary mapping variable names to their descriptions
        """
        return {
            "order_qty": "Order quantities: How much to order for each item at each time period",
            "inventory": "Inventory levels: Stock on hand for each item at each time period",
            "unmet_demand": "Unmet demand: Demand that could not be satisfied for each item at each time period",
            "substitution_flow": "Substitution flow: Amount of demand for item i satisfied by item j at each time period",
        }

    def print_variable_summary(self) -> None:
        """Print a summary of all decision variables and their meanings."""
        print("Decision Variables in the Substitution Model:")
        print("=" * 50)
        descriptions = self.get_variable_descriptions()
        for var_name, description in descriptions.items():
            print(f"• {var_name}: {description}")
        print()


def create_sample_model() -> SubstitutionInventoryOptimizer:
    """Create a sample substitution inventory model for testing."""
    items = ["item1", "item2"]
    days = 5
    demand = {"item1": [100, 120, 110, 130, 115], "item2": [80, 90, 85, 95, 100]}
    substitution_rates = {
        ("item1", "item2"): 0.7,  # 70% of item1 demand can shift to item2
        ("item2", "item1"): 0.5,  # 50% of item2 demand can shift to item1
    }
    costs = {"item1": 2, "item2": 3}
    safety_stock = {"item1": 20, "item2": 15}
    presentation_stock = {"item1": 10, "item2": 5}
    shrink_rates = {"item1": 0.05, "item2": 0.03}
    order_days = [1, 0, 1, 0, 1]  # Can order on days 0, 2, 4

    return SubstitutionInventoryOptimizer(
        items=items,
        days=days,
        demand=demand,
        substitution_rates=substitution_rates,
        costs=costs,
        safety_stock=safety_stock,
        presentation_stock=presentation_stock,
        shrink_rates=shrink_rates,
        order_days=order_days,
        lead_time=1,
    )


if __name__ == "__main__":
    # Example usage
    model = create_sample_model()
    results = model.solve()
    model.print_results()
