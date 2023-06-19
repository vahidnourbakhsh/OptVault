"""DEA math program class for defining the desired DEA model including `primal`, `input_oriented`, and `output_oriented`."""

import pandas as pd
from pyomo.environ import AbstractModel, Set, Param, Var, Objective, Constraint, PositiveReals, NonNegativeReals, Binary, maximize, minimize, inequality, SolverFactory


def _primal_model():
    """ Primal formulation of the DEA model
    """
    TOLERANCE = 0.01 # feasibility tolerance for the normalization constraint below

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
        value = sum(model.invalues[i, unit]*model.target[unit]*model.v[i] for unit in model.Units for i in model.Inputs)
        return inequality(body=value, lower=1-TOLERANCE, upper=1 + TOLERANCE)
    model.normalization = Constraint(rule=normalization_rule)

    return model


def _input_oriented_model():
    """ Input oriented DEA model
    """    
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
    model.theta = Var(within=NonNegativeReals)
    model.lmbda = Var(model.Units, within=NonNegativeReals)

    # Objective
    def theta_rule(model):
        return model.theta
    model.efficiency = Objective(rule=theta_rule, sense=minimize)

    # Constraints
    def input_rule_value(model, input):
        value = sum(model.lmbda[unit] * model.invalues[input, unit] for unit in model.Units) - sum(model.theta * model.target[unit] * model.invalues[input, unit] for unit in model.Units)
        return value

    def input_rule(model, input):
        value = input_rule_value(model, input)
        return inequality(body=value, upper=0)
    model.input_cons = Constraint(model.Inputs, rule=input_rule)


    def output_rule_value(model, output):
        value = sum(model.lmbda[unit] * model.outvalues[output, unit] for unit in model.Units) - sum(model.target[unit] * model.outvalues[output, unit] for unit in model.Units)
        return value

    def output_rule(model, output):
        value = output_rule_value(model, output)
        return inequality(body=value, lower=0)
    model.output_cons = Constraint(model.Outputs, rule=output_rule)

    model.input_rule_value = input_rule_value
    model.output_rule_value = output_rule_value

    return model


def _output_oriented_model():
    """ Output oriented DEA model
    """    
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
    model.theta = Var(within=NonNegativeReals)
    model.lmbda = Var(model.Units, within=NonNegativeReals)

    # Objective
    def theta_rule(model):
        return model.theta
    model.efficiency = Objective(rule=theta_rule, sense=maximize)

    # Constraints
    def input_rule_value(model, input):
        value = sum(model.lmbda[unit] * model.invalues[input, unit] for unit in model.Units) - sum(model.target[unit] * model.invalues[input, unit] for unit in model.Units)
        return value

    def input_rule(model, input):
        value = input_rule_value(model, input)
        return inequality(body=value, upper=0)
    model.input_cons = Constraint(model.Inputs, rule=input_rule)

    def output_rule_value(model, output):
        value = sum(model.lmbda[unit] * model.outvalues[output, unit] for unit in model.Units) - sum(model.theta * model.target[unit] * model.outvalues[output, unit] for unit in model.Units)
        return value

    def output_rule(model, output):
        value = output_rule_value(model, output)
        return inequality(body=value, lower=0)
    model.output_cons = Constraint(model.Outputs, rule=output_rule)

    model.input_rule_value = input_rule_value
    model.output_rule_value = output_rule_value

    def convex_combination_rule(model):
        return sum(model.lmbda[unit] for unit in model.Units) == 1
    model.convex_combination_cons = Constraint(rule=convex_combination_rule)

    return model


class DEAProgram:
    MODELS = {"primal": _primal_model(), "input_oriented": _input_oriented_model(), "output_oriented": _output_oriented_model()}

    def __init__(self, model_type="primal") -> None:
        self.model_type = model_type

    @property
    def model(self) -> AbstractModel:
        return self._create_abstract_model(self.model_type)
    
    def _create_abstract_model(self, model_type="primal") -> AbstractModel:
        return self.MODELS[model_type]

    def get_constraint_status(self, instance, data) -> pd.DataFrame:
        lmbda_sol_values = [0] + [x.value for x in instance.lmbda.values()] 
        theta_sol_values = instance.theta()

        constraint_status = pd.DataFrame(columns=['slack'])
        for input_feature in data[None]["Inputs"][None]:
            slack = round(eval(str(self.model.input_rule_value(instance, input_feature)), {"lmbda": lmbda_sol_values, "theta": theta_sol_values}), 2)
            constraint_status.loc[input_feature] = [slack]
        for output_feature in data[None]["Outputs"][None]:
            slack = round(eval(str(self.model.output_rule_value(instance, output_feature)), {"lmbda": lmbda_sol_values, "theta": theta_sol_values}), 2)
            constraint_status.loc[output_feature] = [slack]

        return constraint_status
