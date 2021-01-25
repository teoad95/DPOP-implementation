from NAryMatrixClass import NAryMatrixRelation
from DpopUtilsClass import join, projection, find_arg_optimal


class Dpop(object):

    def __init__(self, pseudoTree):
        self.PseudoTree = pseudoTree

    def Solve_Problem(self):
        # Util message propagation
        util_message = self.Get_Utils(self.PseudoTree.root, self.PseudoTree.root.get_Child())
        optimal_util_value, optimal_util = find_arg_optimal(self.PseudoTree.root.var, util_message)

        self.PseudoTree.root.var.optimal_value = optimal_util

        # Value message propagation
        self.SendValue(self.PseudoTree.root, optimal_util, self.PseudoTree.root.get_AllChilds())

        # Show results
        for node in self.PseudoTree.PseudoNodes:
            print(node.var.name + ' ' + node.var.optimal_value)

    def Get_Utils(self, parent, nodesToloop):
        utilsFromChildrensArray = []
        for node in nodesToloop:
            if node.get_Child():  # if node has childs get deeper
                util = self.Get_Utils(node, node.get_Child())
            else:
                util = self.CalculateUtil(node)  # return util for the leaf node
            utilsFromChildrensArray.append(util)
        if parent.is_root:
            return self._joinUtilMessagesList(utilsFromChildrensArray)
        return self.CalculateUtil(parent, utilsFromChildrensArray)

    def SendValue(self, sender, util, nodesToLoop):
        for node in nodesToLoop:
            node.ValueMessages[sender.name] = util
        for node in sender.get_Child():
            new_util = self.HandleValue(node)
            self.SendValue(node, new_util, node.get_AllChilds())

    def HandleValue(self, node):
        rel = node.Join.slice(node.ValueMessages)
        values, current_cost = find_arg_optimal(node.var, rel)
        node.var.optimal_value = current_cost
        return current_cost

    def CalculateUtil(self, node, utils_to_join = []):
        for sep in node.get_Seperator():
            variables, constraint = node.compute_binary_constraint(sep)
            constraintArray = NAryMatrixRelation(variables, constraint)
            utils_to_join.append(constraintArray)

        util_message = self._joinUtilMessagesList(utils_to_join)
        node.Join = util_message
        util_message = projection(util_message, node.var)
        print('here')
        return util_message

    def _joinUtilMessagesList(self, utils_to_join):
        util_message = utils_to_join.pop(0)
        for u in utils_to_join:
            util_message = join(util_message, u)
        return util_message
