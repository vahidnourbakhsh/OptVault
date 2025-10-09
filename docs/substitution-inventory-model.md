# Substitution-Based Inventory Optimization

A comprehensive multi-item inventory optimization model that accounts for customer substitution behavior when primary items are out of stock.

## Overview

This model optimizes inventory levels across multiple items while allowing for customer substitutions when primary items are unavailable. It helps retailers maximize service levels while minimizing total costs by accounting for the flexibility customers have in choosing alternative products.

## Business Problem

In retail environments, customers often substitute one product for another when their preferred item is out of stock. Traditional inventory models treat each item independently, missing opportunities to optimize across substitute products. This model captures:

- **Customer substitution patterns** - How likely customers are to accept alternatives
- **Cross-item demand interactions** - How stockouts of one item affect sales of others
- **Service level optimization** - Maintaining availability while minimizing costs
- **Operational constraints** - Order days, lead times, safety stock requirements

## Mathematical Formulation

### Sets and Indices
- $I$: Set of items (e.g., {item1, item2, item3})
- $T$: Set of time periods (e.g., days in planning horizon)
- $i, j \in I$: Items, where $j$ can substitute for $i$
- $t \in T$: Time period

### Parameters
- $D_{it}$: Forecasted demand for item $i$ at time $t$ (from forecasting models like Prophet)
- $S_{ij}$: Substitution rate - fraction of demand for $i$ that shifts to $j$ if $i$ is out of stock ($0 \leq S_{ij} < 1$, $S_{ii} = 0$)
- $L$: Lead time (days between order placement and arrival)
- $O_t$: Binary indicator (1 if orders can be placed at time $t$, 0 otherwise)
- $C_i$: Unit cost of ordering item $i$
- $SS_i$: Safety stock level for item $i$
- $P_i$: Presentation stock (minimum display quantity) for item $i$
- $R_i$: Shrinkage rate for item $i$ (fraction lost per period)
- $M$: Large number (for big-M constraints)
- $Pen$: Penalty cost per unit of unmet demand

### Decision Variables

| Variable | Description | Domain |
|----------|-------------|---------|
| $Q_{it}$ | Order quantity for item $i$ at time $t$ | $\geq 0$ |
| $I_{it}$ | Inventory level of item $i$ at end of time $t$ | $\geq 0$ |
| $U_{it}$ | Unmet demand for item $i$ at time $t$ | $\geq 0$ |
| $F_{ijt}$ | Demand for item $i$ fulfilled by substitute item $j$ at time $t$ | $\geq 0$ |

### Objective Function

Minimize total cost (ordering + penalty for unmet demand):

$$\text{Minimize} \quad \sum_{i \in I} \sum_{t \in T} C_i \cdot Q_{it} + \sum_{i \in I} \sum_{t \in T} Pen \cdot U_{it}$$

### Constraints

#### 1. Inventory Balance
$$I_{i,t} = I_{i,t-1} + Q_{i,t-L} - D_{it} + \sum_{j \neq i} F_{jit} - \sum_{j \neq i} F_{ijt} - R_i \cdot I_{i,t-1}, \quad \forall i, t$$

*Inventory = previous inventory + arrivals - demand + substituted demand received - substituted demand given - shrinkage*

#### 2. Unmet Demand Definition
$$U_{it} \geq D_{it} - I_{i,t-1} - Q_{i,t-L} - \sum_{j \neq i} F_{jit}, \quad \forall i, t$$

*Unmet demand is what remains after using available inventory and receiving substitutions*

#### 3. Substitution Limits
$$F_{ijt} \leq S_{ij} \cdot U_{it}, \quad \forall i, j \neq i, t$$

*Substitution flow is limited by the substitution rate and unmet demand*

#### 4. Minimum Inventory Requirements
$$I_{it} \geq P_i + SS_i, \quad \forall i, t$$

*Inventory must cover presentation and safety stock requirements*

#### 5. Order Day Restrictions
$$Q_{it} \leq M \cdot O_t, \quad \forall i, t$$

*Orders can only be placed on designated order days*

#### 6. Non-negativity
$$Q_{it}, I_{it}, U_{it}, F_{ijt} \geq 0, \quad \forall i, j, t$$

## Implementation

### Quick Start

```python
from optvault.subs import SubstitutionInventoryOptimizer

# Define model parameters
model = SubstitutionInventoryOptimizer(
    items=['product_A', 'product_B', 'product_C'],
    days=7,
    demand={
        'product_A': [120, 135, 140, 125, 130, 110, 95],
        'product_B': [80, 90, 95, 85, 88, 70, 60],
        'product_C': [60, 65, 70, 68, 72, 55, 45]
    },
    substitution_rates={
        ('product_A', 'product_B'): 0.6,  # 60% of A customers accept B
        ('product_B', 'product_C'): 0.5,  # 50% of B customers accept C
        # ... more substitution pairs
    },
    costs={'product_A': 3.50, 'product_B': 2.80, 'product_C': 4.20},
    safety_stock={'product_A': 25, 'product_B': 20, 'product_C': 15},
    order_days=[1, 1, 1, 1, 1, 0, 0],  # Can't order on weekends
    lead_time=1
)

# Solve the optimization problem
results = model.solve()
model.print_results()
```

### Variable Descriptions

The model uses descriptive variable names for clarity:

- **`order_qty`**: How much to order for each item at each time period
- **`inventory`**: Stock on hand for each item at each time period
- **`unmet_demand`**: Demand that couldn't be satisfied for each item
- **`substitution_flow`**: Amount of demand for item i satisfied by item j

## Examples and Tutorials

- **Basic Example**: [`examples/substitution/substitution_example.py`](../../examples/substitution/substitution_example.py)
- **Interactive Tutorial**: See Jupyter notebooks in the examples directory
- **Test Cases**: [`tests/examples/test_substitution.py`](../../tests/examples/test_substitution.py)

## Business Impact

### Benefits of Substitution Modeling

1. **Improved Service Levels**: Better availability through cross-item optimization
2. **Cost Reduction**: Avoid over-ordering by leveraging substitution flexibility
3. **Demand Fulfillment**: Capture sales that would be lost with traditional models
4. **Inventory Efficiency**: Right-size inventory across product families

### Real-World Applications

- **Retail**: Fashion items with size/color substitutions
- **Grocery**: Brand substitutions for similar products
- **Electronics**: Model variations and compatibility
- **Pharmaceuticals**: Generic/brand substitutions

## Model Extensions

The basic model can be extended to include:

- **Time-varying substitution rates**: $S_{ijt}$ instead of $S_{ij}$
- **Capacity constraints**: Maximum order quantities or storage limits
- **Multi-echelon**: Supply chain with multiple locations
- **Stochastic demand**: Uncertainty in demand forecasts
- **Dynamic pricing**: Price-dependent substitution rates

## References and Further Reading

- Cooper, W. W., Seiford, L. M., & Tone, K. (2007). *Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software*
- Nahmias, S. (2008). *Production and Operations Analysis* (6th ed.)
- Silver, E. A., Pyke, D. F., & Peterson, R. (1998). *Inventory Management and Production Planning and Scheduling*

---

*This model is part of the OptVault project - a comprehensive collection of optimization models and tutorials for operations research.*
