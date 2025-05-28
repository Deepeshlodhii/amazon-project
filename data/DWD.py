import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Step 1: Randomly generate integer bounds and objective function for x ∈ R^3
np.random.seed(0)  # For reproducibility

# Random bounds for decision variables x between 1 and 10
lower_bounds = np.random.randint(1, 11, 3)
upper_bounds = lower_bounds + np.random.randint(1, 11, 3)

# Objective function vector c with integer coefficients between -10 and 10
c = np.random.randint(-10, 11, 3)

# Random hyperplane (a, b) for the equality constraint
a = np.random.randint(-10, 11, 3)
b = np.random.randint(-10, 11)

# Print generated parameters
print("Lower bounds:", lower_bounds)
print("Upper bounds:", upper_bounds)
print("Objective function coefficients (c):", c)
print("Equality constraint coefficients (a):", a)
print("Equality constraint constant (b):", b)

# Step 2: Formulating the Master Problem

# Create a Gurobi model for the master problem
def solve_master_problem():
    master_model = gp.Model("MasterProblem")

    # Decision variables x1, x2, x3
    x = master_model.addVars(3, lb=lower_bounds, ub=upper_bounds, name="x")

    # Objective function
    master_model.setObjective(gp.quicksum(c[i] * x[i] for i in range(3)), GRB.MINIMIZE)

    # Equality constraint (a^T x = b)
    master_model.addConstr(gp.quicksum(a[i] * x[i] for i in range(3)) == b, "EqualityConstraint")

    # Non-negativity constraints
    master_model.addConstrs(x[i] >= 0 for i in range(3))

    # Optimize the master problem
    master_model.optimize()

    if master_model.status == GRB.OPTIMAL:
        solution = [x[i].x for i in range(3)]
        print("Master Problem Optimal Solution:", solution)
        print("Objective Value:", master_model.objVal)
    else:
        print("No optimal solution found for the master problem.")

    return master_model

# Solving the master problem
master_model = solve_master_problem()

