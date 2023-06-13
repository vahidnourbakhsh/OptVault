from pyomo.environ import AbstractModel, Set, Param, Var, Objective, Constraint, PositiveReals, NonNegativeReals, Binary, maximize, inequality, SolverFactory

TOLERANCE = 0.01 # feasibility tolerance for the normalization constraint below

model = AbstractModel()
# Sets
model.Inputs = Set()
model.Outputs = Set()
model.Units = Set()

# Parameters
model.invalues = Param(model.Inputs, model.Units, within=PositiveReals)
model.outvalues = Param(model.Outputs, model.Units, within=PositiveReals)
model.target = Param(model.Units, within=Binary)

# Decision vars
model.u = Var(model.Outputs, within=NonNegativeReals)
model.v = Var(model.Inputs, within=NonNegativeReals)

# Objective
def efficiency_rule(model):
    return sum(model.outvalues[j, unit]*model.target[unit]*model.u[j] for unit in model.Units for j in model.Outputs)
model.efficiency = Objective(rule=efficiency_rule, sense=maximize)

# Constraints
def ratio_rule(model, unit):
    value = sum(model.outvalues[j, unit]*model.u[j] for j in model.Outputs) - sum(model.invalues[i, unit]*model.v[i] for i in model.Inputs)
    return inequality(body=value, upper=0)
model.ratio = Constraint(model.Units, rule=ratio_rule)

def normalization_rule(model):
    value = sum(model.invalues[i, unit]*model.target[unit]*model.v[i] for unit in model.Units for i in model.Inputs)
    return inequality(body=value, lower=1-TOLERANCE, upper=1 + TOLERANCE)
model.normalization = Constraint(rule=normalization_rule)