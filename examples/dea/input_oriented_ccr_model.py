""" Primal formulation of the DEA model. This model is mostly useful for explaining DEA model. 
In real cases though we usually solve the dual of this model. Look at input-oriented and output-oriented models.
"""
from pyomo.environ import AbstractModel, Set, Param, Var, Objective, Constraint, PositiveReals, NonNegativeReals, Binary, maximize, minimize, inequality, SolverFactory

model = AbstractModel()

# Sets
model.Inputs = Set()
model.Outputs = Set()
model.Units = Set()

# Parameters
model.invalues = Param(model.Inputs, model.Units, within=NonNegativeReals)
model.outvalues = Param(model.Outputs, model.Units, within=NonNegativeReals)
model.target = Param(model.Units, within=Binary)

# Decision vars
model.u = Var(model.Outputs, within=NonNegativeReals)
model.v = Var(model.Inputs, within=NonNegativeReals)

# Objective
def efficiency_rule(model):
    return sum(model.outvalues[j, unit]*model.target[unit]*model.u[j] for unit in model.Units for j in model.Outputs)
model.efficiency = Objective(rule=efficiency_rule, sense=maximize)


# Constraint
def ratio_rule(model, unit):
    value = sum(model.outvalues[j, unit]*model.u[j] for j in model.Outputs) - sum(model.invalues[i, unit]*model.v[i] for i in model.Inputs)
    return inequality(body=value, upper=0)
model.ratio = Constraint(model.Units, rule=ratio_rule)

def normalization_rule(model):
    return sum(model.invalues[i, unit]*model.target[unit]*model.v[i] for unit in model.Units for i in model.Inputs) == 1
model.normalization = Constraint(rule=normalization_rule)