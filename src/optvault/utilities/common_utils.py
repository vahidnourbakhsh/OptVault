"""Common utility functions for OptVault optimization projects."""

import logging
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

__all__ = [
    "setup_logging",
    "validate_data",
    "load_data_from_file",
    "save_results",
    "calculate_summary_stats",
    "normalize_data",
]


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def validate_data(
    data: pd.DataFrame,
    required_columns: List[str],
    numeric_columns: Optional[List[str]] = None,
) -> bool:
    """Validate input data for optimization models.

    Args:
        data: DataFrame to validate
        required_columns: List of required column names
        numeric_columns: List of columns that should be numeric

    Returns:
        True if validation passes

    Raises:
        ValueError: If validation fails
    """
    # Check required columns
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check numeric columns
    if numeric_columns:
        for col in numeric_columns:
            if col in data.columns and not pd.api.types.is_numeric_dtype(data[col]):
                raise ValueError(f"Column '{col}' must be numeric")

    # Check for empty data
    if data.empty:
        raise ValueError("Data cannot be empty")

    return True


def load_data_from_file(
    filepath: str, file_type: str = "csv", **kwargs
) -> pd.DataFrame:
    """Load data from various file formats.

    Args:
        filepath: Path to the data file
        file_type: Type of file ('csv', 'excel', 'json')
        **kwargs: Additional arguments for pandas read functions

    Returns:
        Loaded DataFrame
    """
    if file_type.lower() == "csv":
        return pd.read_csv(filepath, **kwargs)
    elif file_type.lower() in ["excel", "xlsx", "xls"]:
        return pd.read_excel(filepath, **kwargs)
    elif file_type.lower() == "json":
        return pd.read_json(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def save_results(
    data: Union[pd.DataFrame, Dict[str, Any]],
    filepath: str,
    file_type: str = "csv",
    **kwargs,
) -> None:
    """Save results to file.

    Args:
        data: Data to save (DataFrame or dictionary)
        filepath: Output file path
        file_type: Type of file ('csv', 'excel', 'json')
        **kwargs: Additional arguments for pandas save functions
    """
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    if file_type.lower() == "csv":
        data.to_csv(filepath, index=False, **kwargs)
    elif file_type.lower() in ["excel", "xlsx"]:
        data.to_excel(filepath, index=False, **kwargs)
    elif file_type.lower() == "json":
        data.to_json(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def calculate_summary_stats(
    data: pd.DataFrame, numeric_only: bool = True
) -> pd.DataFrame:
    """Calculate summary statistics for a DataFrame.

    Args:
        data: Input DataFrame
        numeric_only: Whether to include only numeric columns

    Returns:
        DataFrame with summary statistics
    """
    if numeric_only:
        data = data.select_dtypes(include=[np.number])

    return data.describe()


def normalize_data(
    data: pd.DataFrame, method: str = "minmax", columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Normalize data using various methods.

    Args:
        data: Input DataFrame
        method: Normalization method ('minmax', 'zscore', 'robust')
        columns: Specific columns to normalize (default: all numeric)

    Returns:
        Normalized DataFrame
    """
    df = data.copy()

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in columns:
        if method == "minmax":
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        elif method == "zscore":
            df[col] = (df[col] - df[col].mean()) / df[col].std()
        elif method == "robust":
            median = df[col].median()
            mad = (df[col] - median).abs().median()
            df[col] = (df[col] - median) / mad
        else:
            raise ValueError(f"Unknown normalization method: {method}")

    return df
