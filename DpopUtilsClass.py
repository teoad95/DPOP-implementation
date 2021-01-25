from NAryMatrixClass import NAryMatrixRelation


def join(array1, array2):
    dims = array1.dimensions()[:]
    for d2 in array2.dimensions:
        if d2 not in dims:
            dims.append(d2)

    u_j = NAryMatrixRelation(dims, name="joined_utils")
    for ass in _generate_assignment_as_dict(dims):
        u1_ass = _filter_assignment_dict(ass, array1.dimensions)
        u2_ass = _filter_assignment_dict(ass, array2.dimensions)
        s = array1(**u1_ass) + array2(**u2_ass)
        u_j = u_j.set_value_for_assignment(ass, s)

    return u_j


def _generate_assignment_as_dict(variables):
    if len(variables) == 0:
        yield {}
    else:
        current_var = variables[-1]
        for d in current_var.domain:
            for ass in _generate_assignment_as_dict(variables[:-1]):
                ass[current_var.name] = d
                yield ass

def _filter_assignment_dict(assignment, target_vars):
    filtered_ass = {}
    target_vars_names = [v.name for v in target_vars]
    for v in assignment:
        if v in target_vars_names:
            filtered_ass[v] = assignment[v]
    return filtered_ass

def projection(a_rel, a_var):
    remaining_vars = a_rel.dimensions().copy()
    remaining_vars.remove(a_var)

    # the new relation resulting from the projection
    proj_rel = NAryMatrixRelation(remaining_vars)

    for partial in _generate_assignment_as_dict(remaining_vars):
        rel_val = find_arg_optimal(a_var, a_rel.slice(partial))
        proj_rel = proj_rel.set_value_for_assignment(partial, rel_val)

    return proj_rel

def find_arg_optimal(variable, relation):
    for v in variable.domain:
        current_rel_val = relation(v)
        if (best_rel_val < current_rel_val):
            best_rel_val = current_rel_val
    return best_rel_val