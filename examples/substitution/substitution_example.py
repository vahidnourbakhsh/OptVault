"""
Substitution Inventory Optimization Example

This example demonstrates how to use the SubstitutionInventoryOptimizer
to solve multi-item inventory problems with customer substitutions.
"""

import pandas as pd

from optvault.subs import SubstitutionInventoryOptimizer, create_sample_model


def main():
    """Run substitution inventory optimization examples."""

    print("=" * 60)
    print("SUBSTITUTION INVENTORY OPTIMIZATION EXAMPLE")
    print("=" * 60)

    # Example 1: Sample model with default parameters
    print("\n1. Running sample model with default parameters...")
    print("-" * 50)

    sample_model = create_sample_model()
    sample_results = sample_model.solve()
    sample_model.print_results()

    # Example 2: Custom model with more realistic parameters
    print("\n2. Running custom model with realistic parameters...")
    print("-" * 50)

    # Define a more complex scenario
    items = ["product_A", "product_B", "product_C"]
    days = 7  # One week planning horizon

    # Demand forecast (could come from Prophet or other forecasting tools)
    demand = {
        "product_A": [120, 135, 140, 125, 130, 110, 95],  # Weekend lower
        "product_B": [80, 90, 95, 85, 88, 70, 60],
        "product_C": [60, 65, 70, 68, 72, 55, 45],
    }

    # Substitution matrix (customer willingness to substitute)
    substitution_rates = {
        ("product_A", "product_B"): 0.6,  # 60% of A customers accept B
        ("product_A", "product_C"): 0.3,  # 30% of A customers accept C
        ("product_B", "product_A"): 0.4,  # 40% of B customers accept A
        ("product_B", "product_C"): 0.5,  # 50% of B customers accept C
        ("product_C", "product_A"): 0.2,  # 20% of C customers accept A
        ("product_C", "product_B"): 0.7,  # 70% of C customers accept B
    }

    # Costs and constraints
    costs = {"product_A": 3.50, "product_B": 2.80, "product_C": 4.20}
    safety_stock = {"product_A": 25, "product_B": 20, "product_C": 15}
    presentation_stock = {"product_A": 10, "product_B": 8, "product_C": 6}
    shrink_rates = {"product_A": 0.02, "product_B": 0.03, "product_C": 0.01}

    # Order schedule (can't order on weekends)
    order_days = [1, 1, 1, 1, 1, 0, 0]  # Mon-Fri ordering

    # Initial inventory levels
    initial_inventory = {"product_A": 200, "product_B": 150, "product_C": 100}

    custom_model = SubstitutionInventoryOptimizer(
        items=items,
        days=days,
        demand=demand,
        substitution_rates=substitution_rates,
        costs=costs,
        safety_stock=safety_stock,
        presentation_stock=presentation_stock,
        shrink_rates=shrink_rates,
        order_days=order_days,
        lead_time=1,  # 1-day lead time
        initial_inventory=initial_inventory,
        penalty_cost=50.0,  # $50 penalty per unit of unmet demand
    )

    custom_results = custom_model.solve()
    custom_model.print_results()

    # Example 3: Analysis and insights
    print("\n3. Analysis and insights...")
    print("-" * 50)

    # Get results as DataFrame for analysis
    df = custom_model.get_results_dataframe()

    print("\nSummary statistics:")
    print(f"Total optimization cost: ${custom_results['objective_value']:.2f}")

    total_orders = df.groupby("item")["order"].sum()
    total_unmet = df.groupby("item")["unmet_demand"].sum()

    print("\nTotal orders by product:")
    for item, total in total_orders.items():
        print(f"  {item}: {total:.1f} units (${total * costs[item]:.2f})")

    print("\nTotal unmet demand by product:")
    for item, unmet in total_unmet.items():
        service_level = (1 - unmet / sum(demand[item])) * 100
        print(f"  {item}: {unmet:.1f} units ({service_level:.1f}% service level)")

    print("\nSubstitutions made:")
    if custom_results["substitutions"]:
        for (from_item, to_item, day), amount in custom_results[
            "substitutions"
        ].items():
            print(f"  Day {day}: {amount:.1f} units of {from_item} → {to_item}")
    else:
        print("  No substitutions were needed")

    # Example 4: Sensitivity analysis
    print("\n4. Sensitivity analysis - Impact of no substitutions...")
    print("-" * 50)

    # Create model without substitutions for comparison
    no_subs_model = SubstitutionInventoryOptimizer(
        items=items,
        days=days,
        demand=demand,
        substitution_rates={},  # No substitutions allowed
        costs=costs,
        safety_stock=safety_stock,
        presentation_stock=presentation_stock,
        shrink_rates=shrink_rates,
        order_days=order_days,
        lead_time=1,
        initial_inventory=initial_inventory,
        penalty_cost=50.0,
    )

    no_subs_results = no_subs_model.solve()
    no_subs_df = no_subs_model.get_results_dataframe()

    print(f"Cost with substitutions: ${custom_results['objective_value']:.2f}")
    print(f"Cost without substitutions: ${no_subs_results['objective_value']:.2f}")

    savings = no_subs_results["objective_value"] - custom_results["objective_value"]
    print(f"Savings from substitutions: ${savings:.2f}")

    # Compare service levels
    print("\nService level comparison:")
    for item in items:
        with_subs_unmet = df[df["item"] == item]["unmet_demand"].sum()
        without_subs_unmet = no_subs_df[no_subs_df["item"] == item][
            "unmet_demand"
        ].sum()

        total_demand = sum(demand[item])
        service_with = (1 - with_subs_unmet / total_demand) * 100
        service_without = (1 - without_subs_unmet / total_demand) * 100

        print(f"  {item}: {service_with:.1f}% vs {service_without:.1f}%")


if __name__ == "__main__":
    main()
