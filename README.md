# OptVault

This is a collection of optimization models in different fields like transportation, supple chain, pricing, and performance analysis.

## Optimization framework

We use open-source solvers like JuMP, Pyomo, Google OR-tools, and PuLP.

## Example problems

Here are example problems.

### Data Envelopment Analysis (DEA)

DEA is a method used for measuring and comparing performance of different units, usually called Decision Making Units (DMUs).

### Benders decomposition

Benders decomposition is a large-scale optimization technique that iteratively solves a math program. Usually this technique is applied to problems that have special structure and can be decomposed to a main problem and one or more sub-problems. We solve this problem with JuMP since it is easier to get callbacks for dual variables in JuMP than in Pyomo.
