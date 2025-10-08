"""OptVault - A comprehensive collection of optimization models and tutorials.

This package provides practical implementations and educational resources for
various optimization techniques including DEA, supply chain optimization,
transportation problems, and performance analysis.
"""

__version__ = "0.1.0"
__author__ = "OptVault Contributors"

from .utilities import (
    setup_logging,
    validate_data,
    load_data_from_file,
    save_results,
    calculate_summary_stats,
    normalize_data,
)
from .dea import create_dea_model, DEAAnalyzer, TOLERANCE

__all__ = [
    "setup_logging",
    "validate_data",
    "load_data_from_file",
    "save_results",
    "calculate_summary_stats",
    "normalize_data",
    "create_dea_model",
    "DEAAnalyzer",
    "TOLERANCE",
]
