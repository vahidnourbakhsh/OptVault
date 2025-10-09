# Substitution Inventory Optimization Examples

This directory contains examples and tutorials for the substitution-based inventory optimization model.

## Overview

The substitution model optimizes inventory across multiple items while accounting for customer substitution behavior. When a customer's preferred item is out of stock, they may accept an alternative product according to predefined substitution rates.

## Files in this Directory

- **`substitution_example.py`** - Comprehensive example showing basic usage, sensitivity analysis, and business insights
- **Sample data and scenarios** - Various test cases demonstrating different substitution patterns

## Quick Start

```python
from optvault.subs import SubstitutionInventoryOptimizer, create_sample_model

# Option 1: Use the built-in sample model
model = create_sample_model()
results = model.solve()
model.print_results()

# Option 2: Create your own model
model = SubstitutionInventoryOptimizer(
    items=['product_A', 'product_B'],
    days=7,
    demand={'product_A': [100, 110, 120, 115, 105, 90, 80],
            'product_B': [80, 85, 90, 88, 82, 70, 65]},
    substitution_rates={('product_A', 'product_B'): 0.6},
    costs={'product_A': 2.5, 'product_B': 3.0},
    # ... other parameters
)
```

## Key Concepts

### Substitution Rates
- Define the percentage of customers willing to substitute one item for another
- Example: `('item_A', 'item_B'): 0.7` means 70% of item_A customers will accept item_B

### Business Benefits
1. **Improved service levels** through cross-item optimization
2. **Reduced stockouts** by leveraging substitution flexibility
3. **Lower total costs** while maintaining customer satisfaction
4. **Better demand fulfillment** across product families

## Advanced Examples

Run the main example to see:
- Basic optimization
- Sensitivity analysis (with vs. without substitutions)
- Service level comparisons
- Cost impact analysis

```bash
python substitution_example.py
```

## Mathematical Documentation

For detailed mathematical formulation and theory, see:
- [`docs/substitution-inventory-model.md`](../../docs/substitution-inventory-model.md)

## Related Models

This model complements other OptVault models:
- **DEA models** for efficiency analysis
- **Utilities** for data processing and validation
