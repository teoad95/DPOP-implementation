import numpy as np


class NAryMatrixRelation(object):

    def __init__(self, variables, name=""):
        self.Name = name
        self._variables = list(variables)
        shape = tuple([len(v.domain) for v in variables])
        # create a zero-filled matrix
        self._m = np.zeros(shape=shape, dtype=np.float64)

    def set_value_for_assignment(self, var_values, rel_value) -> "NAryMatrixRelation":
        if isinstance(var_values, list):
            _, s = self._slice_matrix([v.name for v in self._variables], var_values)
            matrix = np.copy(self._m)
            matrix[s] = rel_value
            return NAryMatrixRelation(self._variables, matrix, name=self.name)
        elif isinstance(var_values, dict):
            values = []
            for v in self._variables:
                values.append(var_values[v.name])
            _, s = self._slice_matrix([v.name for v in self._variables], values)
            matrix = np.copy(self._m)
            matrix.itemset(s, rel_value)
            return NAryMatrixRelation(self._variables, matrix, name=self.name)
        raise ValueError("Could not set value, must be list or dict")
