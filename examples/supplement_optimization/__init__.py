"""
Supplement Optimization Example

This package contains an implementation of a supplement optimization problem
using linear programming to minimize the total number of pills while meeting
daily nutritional requirements.

IMPORTANT DISCLAIMER:
This tool is for educational and research purposes only. It is NOT intended to
provide medical advice. Always consult with a qualified healthcare provider
before making any changes to your supplement regimen or diet.
"""

from .supplement_optimizer import (
    DailyRequirement,
    Supplement,
    SupplementOptimizer,
    create_sample_data,
)

__all__ = [
    "Supplement",
    "DailyRequirement",
    "SupplementOptimizer",
    "create_sample_data",
]

__version__ = "1.0.0"
