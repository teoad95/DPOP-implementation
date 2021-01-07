import random

class PseudoTree(object):

    def __init__(self, graph):
        self.Graph = graph
        self.PseudoNodes = []

    def PseudoTreeCreation(self):
        nodesAndNeighbours = self.Graph.getNodesAndNeighbours()
        # elect leader randonmly
        root = random.choice(self.Graph.vertices())
        self._AppendNodeToPseudoTree(PseudoTreeNode(root, nodesAndNeighbours[root], True))

    def _AppendNodeToPseudoTree(self, ptn):
        if not ptn in self.PseudoNodes:
            self.PseudoNodes.append(ptn)


class PseudoTreeNode(object):

    def __init__(self, name, nodesAndNeighbours, isRoot = False):
        self.Name = name
        self._P = []
        self._PP = []
        self._C = []
        self._PC = []
        self.IsRoot = isRoot
        self.NodesAndNeighbours = { i : False for i in nodesAndNeighbours }

    def set_Parent(self, x):
        if not x in self._P:
            self._P.append(x)

    def set_PseudoParent(self, x):
        if not x in self._PP:
            self._PP.append(x)

    def set_Child(self, x):
        if not x in self._C:
            self._C.append(x)

    def set_PseudoChild(self, x):
        if not x in self._PC:
            self._PC.append(x)
