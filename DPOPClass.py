from NAryMatrixClass import NAryMatrixRelation
from DpopUtilsClass import join, projection, find_arg_optimal


class Dpop(object):

    def __init__(self, pseudoTree):
        self.PseudoTree = pseudoTree

    def Solve_Proble(self):
        # Util message propagation
        util_message = self.Get_Utils(self.PseudoTree.root, self.PseudoTree.root.get_Child())
        optimal_util_value, optimal_util = find_arg_optimal(self.PseudoTree.root.var, util_message)

        # Value message propagation
        self.SendValue(optimal_util, self.PseudoTree.root.get_Child)

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

    def SendValue(self, util, nodesToLoop):
        for node in nodesToLoop:
            self.HandleValue(node, util)
            if node.get_Child():  # if node has childs get deeper
                self.SendValue(util, node.get_Child())

    def HandleValue(self, node, util):
        # implement the method which will perform whatever it has to do when the node receives the
        # selected value from the root
        pass

    def CalculateUtil(self, node, utils_to_join = []):
        for sep in node.get_Seperator():
            variables, constraint = node.compute_binary_constraint(sep)
            constraintArray = NAryMatrixRelation(variables, constraint)
            utils_to_join.append(constraintArray)

        util_message = self._joinUtilMessagesList(utils_to_join)

        util_message = projection(util_message, node.var)
        print('here')
        return util_message

    def _joinUtilMessagesList(self, utils_to_join):
        util_message = utils_to_join.pop(0)
        for u in utils_to_join:
            util_message = join(util_message, u)
        return util_message
