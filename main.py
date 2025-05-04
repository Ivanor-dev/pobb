import pulp
import math
import sys

class Node:
    def __init__(self, constraints, bounds, depth=0):
        self.constraints = constraints.copy()
        self.bounds = bounds.copy()
        self.depth = depth


def read_problem(file_path):
    with open(file_path, 'r') as f:
        lines = [list(map(int, line.strip().split())) for line in f.readlines() if line.strip()]

    num_vars, num_constraints = lines[0]
    objective = lines[1]
    constraints = []
    for line in lines[2:]:
        constraints.append((line[:-1], line[-1]))
    return num_vars, num_constraints, objective, constraints


def solve_lp(num_vars, objective, constraints, bounds):
    model = pulp.LpProblem("LP_Relaxation", pulp.LpMaximize)
    variables = [pulp.LpVariable(f'x{i}', 0, 1, cat='Continuous') for i in range(num_vars)]

    model += pulp.lpDot(objective, variables)
    for coeffs, rhs in constraints:
        model += (pulp.lpDot(coeffs, variables) <= rhs)

    for var_idx, value in bounds.items():
        if value == 0:
            model += (variables[var_idx] == 0)
        else:
            model += (variables[var_idx] == 1)

    status = model.solve(pulp.PULP_CBC_CMD())

    if status != pulp.LpStatusOptimal:
        return None, None

    solution = [pulp.value(var) for var in variables]
    objective_value = pulp.value(model.objective)
    return solution, objective_value


def select_branch_var(solution):
    fractional_vars = [(i, abs(0.5 - val)) 
                       for i, val in enumerate(solution)
                       if not (math.isclose(val, 0, abs_tol=1e-5) or math.isclose(val, 1, abs_tol=1e-5))]
    if not fractional_vars:
        return None
    
    fractional_vars.sort(key=lambda x: x[1])
    return fractional_vars[0][0]


def is_integral(solution):
    return all(math.isclose(x, 0, abs_tol=1e-5) or math.isclose(x, 1, abs_tol=1e-5) for x in solution)


def branch_and_bound(file_path):
    num_vars, num_constraints, objective, constraints = read_problem(file_path)
    best_solution = None
    best_obj_value = -math.inf

    stack = [Node(constraints, {})]

    while stack:
        node = stack.pop()

        solution, obj_value = solve_lp(num_vars, objective, node.constraints, node.bounds)
        if solution is None:
            continue

        if obj_value <= best_obj_value:
            continue

        if is_integral(solution):
            if obj_value > best_obj_value:
                best_solution = solution
                best_obj_value = obj_value
        else:
            var_to_branch = select_branch_var(solution)
            if var_to_branch is not None:
                bounds0 = node.bounds.copy()
                bounds0[var_to_branch] = 0
                bounds1 = node.bounds.copy()
                bounds1[var_to_branch] = 1
                stack.append(Node(node.constraints, bounds0, node.depth + 1))
                stack.append(Node(node.constraints, bounds1, node.depth + 1))

    return best_solution, best_obj_value


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_entrada>")
    else:
        file_path = sys.argv[1]
        solution, obj_value = branch_and_bound(file_path)

        if solution is None:
            print("Problema inviável")
        else:
            print(f"Melhor valor encontrado: {obj_value}")
            print(f"Solução: {solution}")
