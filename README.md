# OptVault

[![check formatting + run tests](https://github.com/your-username/OptVault/actions/workflows/main.yml/badge.svg)](https://github.com/your-username/OptVault/actions/workflows/main.yml)

## About

**OptVault** is a comprehensive collection of optimization models, tutorials, and utility functions for operations research and mathematical optimization. This repository provides practical implementations and educational resources for various optimization techniques including Data Envelopment Analysis (DEA), supply chain optimization, transportation problems, and performance analysis.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Examples](#examples)
- [Data Envelopment Analysis (DEA)](#data-envelopment-analysis-dea)
- [Utilities](#utilities)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Installation

### Using conda (recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/OptVault.git
cd OptVault

# Create and activate conda environment
conda env create -f environment.yml
conda activate optvault

# Install the package in development mode
pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/your-username/OptVault.git
cd OptVault

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and package
pip install -e .
```

## Features

- **Data Envelopment Analysis (DEA)**: Complete implementation for efficiency analysis
- **Utility Functions**: Common optimization utilities and data processing tools
- **Educational Examples**: Jupyter notebooks with step-by-step implementations
- **Multiple Solvers**: Support for GLPK, OR-Tools, and other open-source solvers
- **Well-tested**: Comprehensive test suite with CI/CD integration

## Examples

All examples are located in the `examples/` directory:

- **`examples/dea/`** - Data Envelopment Analysis tutorials and implementations

## Data Envelopment Analysis (DEA)

DEA is a method used for measuring and comparing performance of different units, usually called Decision Making Units (DMUs).

### 📚 Theory and Implementation

The DEA module (`src/optvault/dea/`) provides:

- **Abstract Model Creation**: Flexible DEA model setup using Pyomo
- **Efficiency Analysis**: Complete workflow for analyzing multiple DMUs
- **Multiple Solver Support**: GLPK, CPLEX, Gurobi compatibility

### 💻 Quick Start

```python
import pandas as pd
from optvault.dea import DEAAnalyzer

# Prepare your data
input_data = pd.DataFrame({
    'DMU1': [2, 3],  # inputs for DMU1
    'DMU2': [4, 2],  # inputs for DMU2
    'DMU3': [3, 4],  # inputs for DMU3
}, index=['Input1', 'Input2'])

output_data = pd.DataFrame({
    'DMU1': [1, 2],  # outputs for DMU1
    'DMU2': [2, 1],  # outputs for DMU2
    'DMU3': [1, 1],  # outputs for DMU3
}, index=['Output1', 'Output2'])

# Run DEA analysis
analyzer = DEAAnalyzer(solver_name='glpk')
results = analyzer.analyze_efficiency(
    input_data,
    output_data,
    ['DMU1', 'DMU2', 'DMU3']
)

print(results)
```

### 📖 Detailed Examples

- **`examples/dea/dea.ipynb`** - Interactive tutorial with complete DEA workflow
- **`examples/dea/dea.py`** - Python script implementation
- **`examples/dea/data/`** - Sample datasets for testing

## Utilities

Essential utility functions for optimization projects are available in `src/optvault/utilities/`:

- **Data Validation**: Robust input validation for optimization models
- **File I/O**: Load/save data in multiple formats (CSV, Excel, JSON)
- **Data Preprocessing**: Normalization, summary statistics, and data cleaning
- **Logging**: Standardized logging setup for optimization workflows

### 💻 Utility Examples

```python
from optvault.utilities import validate_data, normalize_data, load_data_from_file

# Load and validate data
data = load_data_from_file('data.csv')
validate_data(data, required_columns=['input1', 'output1'])

# Normalize data for optimization
normalized_data = normalize_data(data, method='minmax')
```

## Getting Started

1. **Install the package** following the installation instructions above
2. **Explore examples**: Start with `examples/dea/dea.ipynb` for an interactive introduction
3. **Run tests**: Ensure everything works with `pytest tests/`
4. **Check the API**: Import modules and explore available functions

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black src/ tests/ examples/

# Check types
mypy src/
```

## Project Structure

```text
OptVault/
├── src/optvault/           # Main package source code
│   ├── dea/               # Data Envelopment Analysis
│   ├── utilities/         # Common utilities
│   └── __init__.py
├── tests/                 # Test suite
├── examples/              # Example notebooks and scripts
├── docs/                  # Documentation
├── data/                  # Sample datasets
├── environment.yml        # Conda environment
├── pyproject.toml        # Package configuration
└── README.md             # This file
```

## Optimization Framework

We use open-source solvers and frameworks:

- **Pyomo**: Mathematical modeling framework
- **GLPK**: GNU Linear Programming Kit
- **OR-Tools**: Google's optimization tools
- **PuLP**: Python linear programming

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Running tests and code quality checks
- Submitting pull requests
- Code style and documentation standards

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Pyomo](http://www.pyomo.org/) for mathematical modeling
- Inspired by operations research best practices
- Community-driven development and educational focus
