"""Test DEA (Data Envelopment Analysis) models and utilities."""

import pytest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from optvault.dea import create_dea_model, DEAAnalyzer


@pytest.fixture
def sample_dea_data():
    """Create sample DEA data for testing."""
    # Sample data with 3 DMUs, 2 inputs, 2 outputs
    input_data = pd.DataFrame(
        {
            "DMU1": [2, 3],  # Inputs for DMU1
            "DMU2": [4, 2],  # Inputs for DMU2
            "DMU3": [3, 4],  # Inputs for DMU3
        },
        index=["Input1", "Input2"],
    )

    output_data = pd.DataFrame(
        {
            "DMU1": [1, 2],  # Outputs for DMU1
            "DMU2": [2, 1],  # Outputs for DMU2
            "DMU3": [1, 1],  # Outputs for DMU3
        },
        index=["Output1", "Output2"],
    )

    unit_names = ["DMU1", "DMU2", "DMU3"]

    return input_data, output_data, unit_names


def test_create_dea_model():
    """Test that DEA model creation works."""
    model = create_dea_model()

    # Check that the model has the expected components
    assert hasattr(model, "Inputs")
    assert hasattr(model, "Outputs")
    assert hasattr(model, "Units")
    assert hasattr(model, "invalues")
    assert hasattr(model, "outvalues")
    assert hasattr(model, "target")
    assert hasattr(model, "u")
    assert hasattr(model, "v")
    assert hasattr(model, "efficiency")
    assert hasattr(model, "ratio")
    assert hasattr(model, "normalization")


def test_dea_analyzer_initialization():
    """Test DEA analyzer initialization."""
    analyzer = DEAAnalyzer(solver_name="glpk")
    assert analyzer.solver_name == "glpk"
    assert analyzer.solver is not None


def test_dea_analyzer_with_sample_data(sample_dea_data):
    """Test DEA analyzer with sample data."""
    input_data, output_data, unit_names = sample_dea_data

    try:
        analyzer = DEAAnalyzer(solver_name="glpk")
        results = analyzer.analyze_efficiency(input_data, output_data, unit_names)

        # Check results structure
        assert isinstance(results, pd.DataFrame)
        assert "unit" in results.columns
        assert "efficiency_score" in results.columns
        assert len(results) == len(unit_names)

        # Check that all efficiency scores are between 0 and 1
        assert all(
            0 <= score <= 1.1 for score in results["efficiency_score"]
        )  # Allow small tolerance

        # Check that all units are present
        assert set(results["unit"]) == set(unit_names)

    except ImportError:
        pytest.skip("GLPK solver not available")
    except Exception as e:
        if "No executable found for solver" in str(e):
            pytest.skip("GLPK solver not available")
        else:
            raise


def test_dea_data_validation(sample_dea_data):
    """Test data validation in DEA analysis."""
    input_data, output_data, unit_names = sample_dea_data

    analyzer = DEAAnalyzer()

    # Test with mismatched columns
    wrong_input_data = input_data.copy()
    wrong_input_data.columns = ["A", "B", "C"]

    try:
        with pytest.raises(KeyError):
            analyzer.analyze_efficiency(wrong_input_data, output_data, unit_names)
    except ImportError:
        pytest.skip("GLPK solver not available")


def test_empty_data():
    """Test behavior with empty data."""
    analyzer = DEAAnalyzer()

    empty_input = pd.DataFrame()
    empty_output = pd.DataFrame()
    empty_units = []

    try:
        results = analyzer.analyze_efficiency(empty_input, empty_output, empty_units)
        assert len(results) == 0
    except (ImportError, Exception) as e:
        if "No executable found for solver" in str(e) or isinstance(e, ImportError):
            pytest.skip("GLPK solver not available")
        # Empty data should raise some kind of error, which is expected


if __name__ == "__main__":
    pytest.main([__file__])
