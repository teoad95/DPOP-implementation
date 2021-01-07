import random


class PseudoTree(object):

    def __init__(self, graph):
        self.Graph = graph
        self.PseudoNodes = []

    def PseudoTreeCreation(self):
        # elect leader randomly
        root_node = self.elect_root_node()
        # create token
        token = Token(root_node)
        # construct the tree
        self.PseudoTreeNodesCreation(root_node, token)

    def elect_root_node(self):
        root_name = random.choice(self.Graph.vertices())
        root_node = self.CreateNodeAndAddItOnTree(root_name)
        return root_node

    def PseudoTreeNodesCreation(self, parent_node, token):
        for neighbourName in parent_node.Neighbours:

            node_is_parent = next((c for c in parent_node.get_Parent() if c.Name == neighbourName), None)
            if node_is_parent is not None:
                continue

            # may we not really need this check
            node_is_pseudoparent = next((c for c in parent_node.get_PseudoParent() if c.Name == neighbourName), None)
            if node_is_pseudoparent is not None:
                continue

            node_is_pseudochild = next((c for c in parent_node.get_PseudoChild() if c.Name == neighbourName), None)
            if node_is_pseudochild is not None:
                continue

            node_already_exists_in_the_tree = next((c for c in self.PseudoNodes if c.Name == neighbourName), None)
            if node_already_exists_in_the_tree is not None:
                node_already_exists_in_the_tree.set_PseudoChild(parent_node)
                parent_node.set_PseudoParent(node_already_exists_in_the_tree)
            else:
                child_node = self.CreateNodeAndAddItOnTree(neighbourName)
                parent_node.set_Child(child_node)
                child_node.set_Parent(parent_node)
                # Adding child node name to token in order to loop through child's children
                token.HavePassedFrom.append(neighbourName)
                self.PseudoTreeNodesCreation(child_node, token)
                # Removing child node name from token as we finished with child's children and we go one step back
                token.HavePassedFrom.remove(neighbourName)

    def CreateNodeAndAddItOnTree(self, name):
        nodesAndNeighbours = self.Graph.getNodesAndNeighbours()
        rootNode = PseudoTreeNode(name, nodesAndNeighbours[name])
        self._AppendNodeToPseudoTree(rootNode)
        return rootNode

    def _AppendNodeToPseudoTree(self, ptn):
        if not ptn in self.PseudoNodes:
            self.PseudoNodes.append(ptn)


class PseudoTreeNode(object):

    def __init__(self, name, neighbours):
        self.Name = name
        self._P = []
        self._PP = []
        self._C = []
        self._PC = []
        self.Neighbours = neighbours

    def set_Parent(self, x):
        if not x in self._P:
            self._P.append(x)

    def get_Parent(self):
        return self._P

    def set_PseudoParent(self, x):
        if not x in self._PP:
            self._PP.append(x)

    def get_PseudoParent(self):
        return self._PP

    def set_Child(self, x):
        if not x in self._C:
            self._C.append(x)

    def get_Child(self):
        return self._C

    def set_PseudoChild(self, x):
        if not x in self._PC:
            self._PC.append(x)

    def get_PseudoChild(self):
        return self._PC


class Token(object):

    def __init__(self, ParentNodes):
        self.HavePassedFrom = []
        self.HavePassedFrom.append(ParentNodes)
