from PseudoTreeClass import PseudoTree

class Dpop(object):

    def __init__(self, pseudoTree):
        self.PseudoTree = pseudoTree

    def Solve_Proble(self):
        # TODO order tree nodes this may already be implemented

        # Util message propagation
        util = self.ChooseOptimalUtil(self.Get_Utils(self.PseudoTree.root.get_Child))

        # Value message propagation
        self.SendValue(util, self.PseudoTree.root.get_Child)

    def Get_Utils(self, nodesToloop):
        utilsArray = []
        for node in nodesToloop:
            if node.get_Child: # if node has childs get deeper
                util = self.Get_Utils(node.get_Child)
            else:
                return self.CalculateUtil(node) # return util for the leaf node
            self.JoinArrays(utilsArray, util)
        # here we will have to do whatever we need to do when the node receives all the utils from childs
        return utilsArray

    def SendValue(self, util, nodesToLoop):
        for node in nodesToLoop:
            if node.get_Child:  # if node has childs get deeper
                self.SendValue(util, node.get_Child)
            self.HandleValue(node, util)

    def HandleValue(self, node, util):
        # implement the method which will perform whatever it has to do when the node receives the
        # selected value from the root
        pass

    def JoinArrays(self, utilsArray, util):
        # implement the method which will join the arrays
        pass

    def CalculateUtil(self, node):
        # implement the method which will calculate the utils
        pass

    def ChooseOptimalUtil(self, param):
        # implement the method which will choose the optimal util
        pass