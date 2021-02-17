import numpy as np


class NAryMatrixRelation(object):

    def __init__(self, variables, matrix=None, name=""):
        self.name = name
        self._variables = list(variables)
        shape = tuple([len(v.domain) for v in variables])
        # create a zero-filled matrix
        if matrix is None:
            # create a zero-filled matrix
            self._m = np.zeros(shape=shape, dtype=np.float64)

        else:
            if not isinstance(matrix, np.array.__class__):
                matrix = np.array(matrix)
            if shape != matrix.shape:
                raise AttributeError(
                    "Invalid dimension when building util " "from matrix"
                )
            self._m = matrix

    def GetUtilMessageNumberOfDimensions(self):
        return self._m.shape.__len__()

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

    def dimensions(self)  :
        return  self._variables

    def slice(
            self, partial_assignment, ignore_extra_vars=False
    ) -> "NAryMatrixRelation":
        if not partial_assignment:
            return self
        sliced_vars, sliced_values = zip(*partial_assignment.items())
        slice_vars, s = self._slice_matrix(
            sliced_vars, sliced_values, ignore_extra_vars=ignore_extra_vars
        )
        u = NAryMatrixRelation(slice_vars, self._m[s], self.name)
        return u

    def _slice_matrix(self, sliced_vars, sliced_values, ignore_extra_vars=False):

        s_vars = list(sliced_vars)
        s_values = list(sliced_values)

        var_names = [v.name for v in self._variables]
        for i, v in enumerate(sliced_vars):
            if v not in var_names:
                if not ignore_extra_vars:
                    raise AttributeError(
                        "{} is not in the dimensions of util : {}".format(
                            v, self._variables
                        )
                    )
                else:
                    del s_vars[i]
                    del s_values[i]

        slices = []
        slice_vars = []
        for v in self._variables:
            if v.name in s_vars:
                slice_index = s_vars.index(v.name)
                val = s_values[slice_index]
                val_index = v.domain.index(val)
                slices.append(val_index)
            else:
                slices.append(slice(None))
                slice_vars.append(v)

        return slice_vars, tuple(slices)

    def __call__(self, *args, **kwargs):
        """
        Shortcut method for get_value_for_assignment.
        Instead of using `relation.get_value_for_assignment([val1, val2,
        ...])` you can use the relation as a callable and directly use
        `relation(val1, val2, ...)`
        :param args: values representing a full assignment of
        the variables of the relation, in the same order as the variables in
        the dimension.
        :return: the value of the relation.
        """

        if not kwargs:
            return self.get_value_for_assignment(list(args))
        else:
            return self.get_value_for_assignment(kwargs)


    def get_value_for_assignment(self, var_values=None):
        """
        Returns the value of the relation for an assignment.
        :param var_values: either a list or a dict.
        * If var_values is a list, it must be  an array of values
        representing a full assignment of the variables of the relation,
        in the same order as the variables in the dimension.
        * If it is a dict, it must be a var_name => var_value mapping
        :return: the value of the relation.
        """

        if var_values is None:
            if self._m.shape == ():
                return self._m
            else:
                raise KeyError(
                    "Needs an assignement when requesting value "
                    "in a n-ari relation, n!=0"
                )
        if isinstance(var_values, list):
            assignt = {self._variables[i].name: val for i, val in enumerate(var_values)}
            u = self.slice(assignt)
            return u._m.item()

        elif isinstance(var_values, dict):
            u = self.slice(var_values)
            return u._m.item()

        else:
            raise ValueError("Assignment must be dict or array")