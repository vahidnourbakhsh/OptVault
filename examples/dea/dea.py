from pyomo.environ import *
infinity = float('inf')

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

def normalization_rule(model, unit):
    return sum(model.invalues[i, unit]*model.v[i] for i in model.Inputs) == 1
model.normalization = Constraint(model.Units, rule=normalization_rule)
