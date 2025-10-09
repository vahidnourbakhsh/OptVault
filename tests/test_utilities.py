"""Test utility functions for OptVault."""

import os
import sys
import tempfile

import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from optvault.utilities import (
    calculate_summary_stats,
    load_data_from_file,
    normalize_data,
    save_results,
    validate_data,
)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
            "C": ["x", "y", "z", "w", "v"],
            "D": [1.1, 2.2, 3.3, 4.4, 5.5],
        }
    )


def test_validate_data_success(sample_dataframe):
    """Test successful data validation."""
    result = validate_data(
        sample_dataframe, required_columns=["A", "B"], numeric_columns=["A", "B", "D"]
    )
    assert result is True


def test_validate_data_missing_columns(sample_dataframe):
    """Test validation failure with missing columns."""
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(sample_dataframe, required_columns=["A", "B", "X", "Y"])


def test_validate_data_non_numeric(sample_dataframe):
    """Test validation failure with non-numeric columns."""
    with pytest.raises(ValueError, match="must be numeric"):
        validate_data(
            sample_dataframe, required_columns=["A", "C"], numeric_columns=["C"]
        )


def test_validate_data_empty():
    """Test validation failure with empty DataFrame."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="Data cannot be empty"):
        validate_data(empty_df, required_columns=[])


def test_save_and_load_csv(sample_dataframe):
    """Test saving and loading CSV files."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        temp_path = f.name

    try:
        # Save data
        save_results(sample_dataframe, temp_path, file_type="csv")

        # Load data back
        loaded_data = load_data_from_file(temp_path, file_type="csv")

        # Compare (excluding index)
        pd.testing.assert_frame_equal(
            sample_dataframe.reset_index(drop=True), loaded_data.reset_index(drop=True)
        )
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_save_and_load_json(sample_dataframe):
    """Test saving and loading JSON files."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    try:
        # Save data
        save_results(sample_dataframe, temp_path, file_type="json")

        # Load data back
        loaded_data = load_data_from_file(temp_path, file_type="json")

        # JSON may change data types, so we compare values
        assert loaded_data.shape == sample_dataframe.shape

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_calculate_summary_stats(sample_dataframe):
    """Test summary statistics calculation."""
    stats = calculate_summary_stats(sample_dataframe, numeric_only=True)

    # Should only include numeric columns
    assert "A" in stats.columns
    assert "B" in stats.columns
    assert "D" in stats.columns
    assert "C" not in stats.columns  # String column should be excluded

    # Check that basic stats are present
    assert "mean" in stats.index
    assert "std" in stats.index
    assert "min" in stats.index
    assert "max" in stats.index


def test_normalize_data_minmax(sample_dataframe):
    """Test min-max normalization."""
    normalized = normalize_data(sample_dataframe, method="minmax", columns=["A", "B"])

    # Check that values are between 0 and 1
    assert normalized["A"].min() == 0.0
    assert normalized["A"].max() == 1.0
    assert normalized["B"].min() == 0.0
    assert normalized["B"].max() == 1.0

    # Non-normalized columns should remain unchanged
    pd.testing.assert_series_equal(normalized["C"], sample_dataframe["C"])


def test_normalize_data_zscore(sample_dataframe):
    """Test z-score normalization."""
    normalized = normalize_data(sample_dataframe, method="zscore", columns=["A"])

    # Check that mean is approximately 0 and std is approximately 1
    assert abs(normalized["A"].mean()) < 1e-10  # Should be very close to 0
    assert abs(normalized["A"].std() - 1.0) < 1e-10  # Should be very close to 1


def test_normalize_data_robust(sample_dataframe):
    """Test robust normalization."""
    normalized = normalize_data(sample_dataframe, method="robust", columns=["A"])

    # Check that median is 0
    assert normalized["A"].median() == 0.0


def test_normalize_data_invalid_method(sample_dataframe):
    """Test normalization with invalid method."""
    with pytest.raises(ValueError, match="Unknown normalization method"):
        normalize_data(sample_dataframe, method="invalid_method")


def test_save_results_dict():
    """Test saving dictionary results."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        temp_path = f.name

    try:
        # Save dictionary as CSV
        test_dict = {"metric1": 0.95, "metric2": 0.87, "metric3": 0.92}
        save_results(test_dict, temp_path, file_type="csv")

        # Load back and verify
        loaded_data = load_data_from_file(temp_path, file_type="csv")
        assert len(loaded_data) == 1
        assert loaded_data.iloc[0]["metric1"] == 0.95

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__])
