# Supplement Optimization Example

This example demonstrates how to solve a supplement optimization problem using linear programming. The goal is to find the minimum number of pills/capsules/tablets to take while meeting daily nutritional requirements.

## ⚠️ IMPORTANT DISCLAIMER

**This tool is for educational and research purposes only.** It is NOT intended to provide medical advice, diagnosis, or treatment recommendations.

**ALWAYS consult with a qualified healthcare provider, registered dietitian, or physician before making any changes to your supplement regimen or diet.** Individual nutritional needs vary based on:

- Age, gender, and life stage
- Health conditions and medical history
- Medications and drug interactions
- Activity level and lifestyle
- Genetic factors
- Pregnancy, breastfeeding, or other special conditions

**The authors and contributors assume NO RESPONSIBILITY for any health consequences resulting from the use of this tool.** This model cannot account for individual medical needs, contraindications, or supplement interactions.

## Problem Description

Given:

- A set of available supplements, each with different nutritional content
- Daily nutritional requirements for a person
- Goal: Minimize the total number of pills while meeting all requirements

This is a variant of the classic "diet problem" in operations research.

## Mathematical Formulation

**Decision Variables:**

- `x_i` = number of units of supplement `i` to take

**Objective Function:**

```text
Minimize: Σ x_i  (total number of pills)
```

**Constraints:**

```text
Σ (nutritional_content_ij * x_i) ≥ daily_requirement_j  for all nutrients j
x_i ≥ 0  for all supplements i
```

## Features

- **Multiple Optimization Objectives:**
  - Minimize total number of pills
  - Minimize total cost
  - Integer solutions (whole pills only)

- **Flexible Input:**
  - Custom supplement database
  - Personalized daily requirements
  - Support for different supplement forms (pills, capsules, gummies)

- **Comprehensive Analysis:**
  - Detailed nutrient breakdown
  - Surplus analysis
  - Cost breakdown (when available)

## Usage

```python
from supplement_optimizer import SupplementOptimizer, Supplement, DailyRequirement

# Create optimizer
optimizer = SupplementOptimizer()

# Add supplements
optimizer.add_supplement(Supplement(
    name="Multivitamin",
    brand="NatureMade",
    form="tablet",
    nutrients={"Vitamin C": 90, "Calcium": 162, "Iron": 8},
    cost_per_unit=0.15
))

# Set daily requirements
daily_req = DailyRequirement(
    age=35,
    gender="male",
    requirements={"Vitamin C": 90, "Calcium": 1000, "Iron": 8}
)
optimizer.set_daily_requirements(daily_req)

# Solve optimization problem
result = optimizer.solve_minimum_pills()
optimizer.print_solution(result)
```

## Example Output

```text
✅ Optimal solution found: 2.340 total pills/units

📋 Daily Requirements: Male, age 35
💊 Total Pills/Units: 2.34

📝 Supplement Plan:
  • 1.0 tablet(s) of NatureMade Multivitamin
  • 0.5 tablet(s) of Kirkland Calcium + D3
  • 1.0 capsule(s) of Nordic Naturals Omega-3

🔬 Nutrient Analysis:
  • Vitamin C: 90.0/90 (100.0%)
  • Calcium: 1000.0/1000 (100.0%)
  • Iron: 8.0/8 (100.0%)
  • Omega-3 EPA: 325.0/250 (130.0%) (+75.0 surplus)
```

## Running the Example

### Python Script

```bash
cd examples/supplement_optimization
python supplement_optimizer.py
```

### Interactive Jupyter Notebook

For an interactive exploration of the model:

```bash
cd examples/supplement_optimization
jupyter notebook supplement_optimization_demo.ipynb
```

The Jupyter notebook includes:

- Step-by-step walkthrough of the optimization process
- Interactive visualizations of results
- Custom scenario examples (athlete requirements, budget constraints)
- Charts comparing different optimization strategies

Both will run demonstrations with sample supplements and requirements, showing optimization results for:

1. Minimum number of pills
2. Minimum cost
3. Integer solutions (whole pills only)

## Dependencies

- `numpy`: For numerical computations
- `scipy`: For linear programming solver
- `typing`: For type hints
- `dataclasses`: For structured data representation

## Extensions

Possible extensions to this model:

- Add maximum daily limits for nutrients (upper bounds)
- Include nutrient interaction effects
- Add preference weights for different supplement forms
- Support for time-based dosing (morning vs evening)
- Integration with supplement databases or APIs
- Sensitivity analysis for requirement changes
