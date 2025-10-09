# Contributing to OptVault

Thank you for your interest in contributing to OptVault! This document provides guidelines and information for contributors.

## Getting Started

### Development Environment Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/OptVault.git
   cd OptVault
   ```

2. **Create a conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate optvault
   ```

3. **Install the package in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install additional development tools**
   ```bash
   # Install pre-commit hooks (optional but recommended)
   pip install pre-commit
   pre-commit install
   ```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and checks**
   ```bash
   # Run tests
   pytest tests/

   # Format code
   black src/ tests/ examples/

   # Check types (optional)
   mypy src/
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting (line length: 88)
- Add type hints for function parameters and return values
- Write descriptive docstrings for all public functions and classes

### Example Code Style

```python
def calculate_efficiency(
    input_values: pd.DataFrame,
    output_values: pd.DataFrame,
    target_unit: str,
    solver_name: str = "glpk"
) -> float:
    """Calculate efficiency score for a target DMU using DEA.

    Args:
        input_values: DataFrame with input data for all DMUs
        output_values: DataFrame with output data for all DMUs
        target_unit: Name of the DMU to analyze
        solver_name: Name of the optimization solver to use

    Returns:
        Efficiency score between 0 and 1

    Raises:
        ValueError: If target_unit is not found in the data
    """
    # Implementation here
    pass
```

### Documentation Style

- Use clear, concise language
- Include code examples in docstrings
- Follow [Google docstring format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Update README.md for significant new features

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use pytest framework
- Follow the naming convention: `test_<functionality>.py`
- Include both positive and negative test cases
- Use fixtures for common test data

### Test Structure

```python
import pytest
import pandas as pd
from optvault.module import function_to_test

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame(...)

def test_function_success(sample_data):
    """Test successful function execution."""
    result = function_to_test(sample_data)
    assert result is not None
    # More assertions...

def test_function_error_handling():
    """Test error handling."""
    with pytest.raises(ValueError):
        function_to_test(invalid_input)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_dea.py

# Run with coverage
pytest tests/ --cov=src/optvault --cov-report=html
```

## Adding New Features

### New Optimization Models

When adding a new optimization model:

1. Create a new subdirectory in `src/optvault/`
2. Implement the model with proper error handling
3. Add comprehensive tests
4. Create example notebook in `examples/`
5. Update package `__init__.py` and documentation

### Directory Structure for New Models

```text
src/optvault/new_model/
├── __init__.py
├── model_implementation.py
└── utilities.py (if needed)

tests/
└── test_new_model.py

examples/new_model/
├── new_model.ipynb
├── data/
└── README.md
```

## Documentation

### Adding Examples

- Create Jupyter notebooks with clear explanations
- Include sample data in `examples/*/data/`
- Add README.md for each example directory
- Use markdown cells to explain concepts

### Updating Documentation

- Update README.md for new features
- Add docstrings to all public functions
- Include usage examples in docstrings
- Update this CONTRIBUTING.md if workflow changes

## Commit Message Guidelines

Use conventional commits format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring
- `style:` for formatting changes
- `chore:` for maintenance tasks

Examples:
```
feat: add support for robust DEA models
fix: handle edge case in efficiency calculation
docs: update README with installation instructions
test: add tests for data validation utilities
```

## Pull Request Process

### Before Submitting

1. Ensure all tests pass
2. Update documentation
3. Add tests for new functionality
4. Run code formatting tools
5. Update CHANGELOG.md (if exists)

### Pull Request Description

Include in your PR description:

- **What**: Brief description of changes
- **Why**: Motivation for the changes
- **How**: Technical details if complex
- **Testing**: How you tested the changes
- **Breaking Changes**: Any backwards incompatible changes

### Review Process

1. Automated checks must pass (CI/CD)
2. Code review by maintainers
3. Address review feedback
4. Final approval and merge

## Issue Reporting

### Bug Reports

Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Error messages and tracebacks
- Minimal code example

### Feature Requests

Include:
- Use case description
- Proposed API or interface
- Examples of usage
- Implementation suggestions (optional)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow professional communication standards

## Getting Help

- Check existing issues and documentation first
- Ask questions in GitHub issues
- Join discussions in pull requests
- Contact maintainers for complex questions

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributor statistics

Thank you for contributing to OptVault!
