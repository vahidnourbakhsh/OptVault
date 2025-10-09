"""Test substitution-based inventory optimization models."""

import os
import sys

import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from optvault.subs import SubstitutionInventoryOptimizer, create_sample_model


@pytest.fixture
def simple_subs_data():
    """Create simple substitution model data for testing."""
    items = ["item1", "item2"]
    days = 3  # Shorter horizon for testing
    demand = {"item1": [50.0, 60.0, 55.0], "item2": [40.0, 45.0, 50.0]}
    substitution_rates = {("item1", "item2"): 0.5, ("item2", "item1"): 0.3}
    costs = {"item1": 1.0, "item2": 1.5}
    safety_stock = {"item1": 10.0, "item2": 8.0}
    presentation_stock = {"item1": 5.0, "item2": 3.0}
    shrink_rates = {"item1": 0.01, "item2": 0.02}
    order_days = [1, 1, 1]  # Can order every day for simplicity

    return {
        "items": items,
        "days": days,
        "demand": demand,
        "substitution_rates": substitution_rates,
        "costs": costs,
        "safety_stock": safety_stock,
        "presentation_stock": presentation_stock,
        "shrink_rates": shrink_rates,
        "order_days": order_days,
        "lead_time": 0,  # No lead time for simplicity
        "initial_inventory": {"item1": 100.0, "item2": 80.0},  # High initial inventory
    }


def test_substitution_model_initialization(simple_subs_data):
    """Test that substitution model can be initialized."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)

    assert model.items == simple_subs_data["items"]
    assert model.days == simple_subs_data["days"]
    assert model.demand == simple_subs_data["demand"]
    assert model.substitution_rates == simple_subs_data["substitution_rates"]


def test_substitution_model_build(simple_subs_data):
    """Test that substitution model can be built."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    model.build_model()

    assert model.problem is not None
    assert "order_qty" in model.variables
    assert "inventory" in model.variables
    assert "unmet_demand" in model.variables
    assert "substitution_flow" in model.variables


def test_substitution_model_solve(simple_subs_data):
    """Test that substitution model can be solved."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    results = model.solve()

    assert "status" in results
    assert "objective_value" in results
    assert "orders" in results
    assert "inventory" in results
    assert "unmet_demand" in results
    assert "substitutions" in results


def test_substitution_model_results_dataframe(simple_subs_data):
    """Test that results can be converted to DataFrame."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    model.solve()

    df = model.get_results_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert "day" in df.columns
    assert "item" in df.columns
    assert "order" in df.columns
    assert "inventory" in df.columns
    assert "unmet_demand" in df.columns
    assert len(df) == simple_subs_data["days"] * len(simple_subs_data["items"])


def test_create_sample_model():
    """Test the sample model creation function."""
    model = create_sample_model()

    assert isinstance(model, SubstitutionInventoryOptimizer)
    assert len(model.items) == 2
    assert model.days == 5

    # Test that it can solve
    results = model.solve()
    assert "status" in results


def test_substitution_constraints(simple_subs_data):
    """Test that substitution constraints are working correctly."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    results = model.solve()

    # Check that substitutions don't exceed the defined rates
    for (from_item, to_item, day), sub_amount in results["substitutions"].items():
        unmet_demand = results["unmet_demand"][(from_item, day)]
        max_substitution = (
            simple_subs_data["substitution_rates"][(from_item, to_item)] * unmet_demand
        )
        assert (
            sub_amount <= max_substitution + 1e-6
        )  # Small tolerance for numerical precision


def test_inventory_non_negative(simple_subs_data):
    """Test that inventory levels are non-negative."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    results = model.solve()

    for (item, day), inventory in results["inventory"].items():
        # Allow small negative values due to numerical precision, but flag large ones
        if inventory < -1e-3:
            pytest.fail(f"Negative inventory for {item} on day {day}: {inventory}")


def test_order_quantities_non_negative(simple_subs_data):
    """Test that order quantities are non-negative."""
    model = SubstitutionInventoryOptimizer(**simple_subs_data)
    results = model.solve()

    for (item, day), order in results["orders"].items():
        assert order >= -1e-6, f"Negative order for {item} on day {day}: {order}"


def test_model_with_no_substitutions():
    """Test model behavior with no substitutions allowed."""
    data = {
        "items": ["item1", "item2"],
        "days": 2,
        "demand": {"item1": [30.0, 35.0], "item2": [25.0, 30.0]},
        "substitution_rates": {},  # No substitutions
        "costs": {"item1": 1.0, "item2": 1.0},
        "safety_stock": {"item1": 5.0, "item2": 5.0},
        "presentation_stock": {"item1": 2.0, "item2": 2.0},
        "shrink_rates": {"item1": 0.0, "item2": 0.0},  # No shrinkage
        "order_days": [1, 1],
        "lead_time": 0,
        "initial_inventory": {"item1": 50.0, "item2": 50.0},
    }

    model = SubstitutionInventoryOptimizer(**data)
    results = model.solve()

    # Should have no substitutions
    assert len(results["substitutions"]) == 0
    assert "status" in results
