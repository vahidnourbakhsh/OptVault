"""Data Envelopment Analysis (DEA) models and utilities.

This module provides implementations for DEA optimization models using Pyomo.
DEA is a method used for measuring and comparing performance of different units,
usually called Decision Making Units (DMUs).
"""

from pyomo.environ import (
    AbstractModel,
    Set,
    Param,
    Var,
    Objective,
    Constraint,
    PositiveReals,
    NonNegativeReals,
    Binary,
    maximize,
    inequality,
    SolverFactory,
    value,
)
import pandas as pd
from typing import List


TOLERANCE = 0.01  # feasibility tolerance for the normalization constraint


def create_dea_model() -> AbstractModel:
    """Create and return a DEA abstract model.

    Returns:
        AbstractModel: Pyomo abstract model for DEA optimization
    """
    model = AbstractModel()

    # Sets
    model.Inputs = Set()
    model.Outputs = Set()
    model.Units = Set()

    # Parameters
    model.invalues = Param(model.Inputs, model.Units, within=PositiveReals)
    model.outvalues = Param(model.Outputs, model.Units, within=PositiveReals)
    model.target = Param(model.Units, within=Binary)

    # Decision vars
    model.u = Var(model.Outputs, within=NonNegativeReals)
    model.v = Var(model.Inputs, within=NonNegativeReals)

    # Objective
    def efficiency_rule(model):
        return sum(
            model.outvalues[j, unit] * model.target[unit] * model.u[j]
            for unit in model.Units
            for j in model.Outputs
        )

    model.efficiency = Objective(rule=efficiency_rule, sense=maximize)

    # Constraints
    def ratio_rule(model, unit):
        value = sum(model.outvalues[j, unit] * model.u[j] for j in model.Outputs) - sum(
            model.invalues[i, unit] * model.v[i] for i in model.Inputs
        )
        return inequality(body=value, upper=0)

    model.ratio = Constraint(model.Units, rule=ratio_rule)

    def normalization_rule(model):
        value = sum(
            model.invalues[i, unit] * model.target[unit] * model.v[i]
            for unit in model.Units
            for i in model.Inputs
        )
        return inequality(body=value, lower=1 - TOLERANCE, upper=1 + TOLERANCE)

    model.normalization = Constraint(rule=normalization_rule)

    return model


class DEAAnalyzer:
    """DEA Analyzer class for running efficiency analysis on multiple DMUs."""

    def __init__(self, solver_name: str = "glpk"):
        """Initialize DEA analyzer.

        Args:
            solver_name: Name of the solver to use (default: 'glpk')
        """
        self.solver_name = solver_name
        self.solver = SolverFactory(solver_name)

    def analyze_efficiency(
        self, input_data: pd.DataFrame, output_data: pd.DataFrame, unit_names: List[str]
    ) -> pd.DataFrame:
        """Analyze efficiency for all DMUs.

        Args:
            input_data: DataFrame with input values (units as columns, inputs as rows)
            output_data: DataFrame with output values (units as columns, outputs as rows)
            unit_names: List of unit names to analyze

        Returns:
            DataFrame with efficiency scores for each unit
        """
        results = []

        for unit in unit_names:
            efficiency_score = self._solve_for_unit(
                input_data, output_data, unit_names, unit
            )
            results.append({"unit": unit, "efficiency_score": efficiency_score})

        return pd.DataFrame(results)

    def _solve_for_unit(
        self,
        input_data: pd.DataFrame,
        output_data: pd.DataFrame,
        unit_names: List[str],
        target_unit: str,
    ) -> float:
        """Solve DEA model for a specific target unit.

        Args:
            input_data: DataFrame with input values
            output_data: DataFrame with output values
            unit_names: List of all unit names
            target_unit: Name of the unit to analyze

        Returns:
            Efficiency score for the target unit
        """
        model = create_dea_model()

        # Create data dictionary for the model
        data = {
            "Inputs": list(input_data.index),
            "Outputs": list(output_data.index),
            "Units": unit_names,
        }

        # Add input values
        data["invalues"] = {}
        for inp in input_data.index:
            for unit in unit_names:
                data["invalues"][inp, unit] = input_data.loc[inp, unit]

        # Add output values
        data["outvalues"] = {}
        for out in output_data.index:
            for unit in unit_names:
                data["outvalues"][out, unit] = output_data.loc[out, unit]

        # Set target unit
        data["target"] = {unit: 1 if unit == target_unit else 0 for unit in unit_names}

        # Create instance and solve
        instance = model.create_instance(data)
        results = self.solver.solve(instance)

        if results.solver.termination_condition.name == "optimal":
            return value(instance.efficiency)
        else:
            raise RuntimeError(
                f"Solver failed for unit {target_unit}: {results.solver.termination_condition}"
            )


__all__ = ["create_dea_model", "DEAAnalyzer", "TOLERANCE"]
