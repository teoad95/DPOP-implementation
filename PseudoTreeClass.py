import random
import numpy as np
from anytree import NodeMixin, PostOrderIter

class PseudoTree(object):

    def __init__(self, graph, variable_x_unary_constraint):
        self.Graph = graph
        self.variable_x_unary_constraint = variable_x_unary_constraint
        self.PseudoNodes = []
        self.root = None

    def PseudoTreeCreation(self):
        # elect leader randomly
        root_node = self.elect_root_node()
        self.root = root_node
        # create token
        # token = Token(root_node)
        # construct the tree
        self.PseudoTreeNodesCreation(root_node)
        self.compute_node_seperators()

    def elect_root_node(self):
        root_name = random.choice(self.Graph.vertices())
        root_node = self.CreateNodeAndAddItOnTree(root_name, parent_node=None)
        return root_node

    def PseudoTreeNodesCreation(self, parent_node):
        for neighbourName in parent_node.Neighbours:

            node_is_parent = next((c for c in parent_node.get_Parent() if c.name == neighbourName), None)
            if node_is_parent is not None:
                continue

            # may we not really need this check
            node_is_pseudoparent = next((c for c in parent_node.get_PseudoParent() if c.name == neighbourName), None)
            if node_is_pseudoparent is not None:
                continue

            node_is_pseudochild = next((c for c in parent_node.get_PseudoChild() if c.name == neighbourName), None)
            if node_is_pseudochild is not None:
                continue

            node_already_exists_in_the_tree = next((c for c in self.PseudoNodes if c.name == neighbourName), None)
            if node_already_exists_in_the_tree is not None:
                node_already_exists_in_the_tree.set_PseudoChild(parent_node)
                parent_node.set_PseudoParent(node_already_exists_in_the_tree)
            else:
                child_node = self.CreateNodeAndAddItOnTree(neighbourName, parent_node)
                parent_node.set_Child(child_node)
                child_node.set_Parent(parent_node)
                # Adding child node name to token in order to loop through child's children
                # token.HavePassedFrom.append(neighbourName)
                self.PseudoTreeNodesCreation(child_node)
                # Removing child node name from token as we finished with child's children and we go one step back
                # token.HavePassedFrom.remove(neighbourName)

    def CreateNodeAndAddItOnTree(self, name, parent_node):
        nodesAndNeighbours = self.Graph.getNodesAndNeighbours()
        rootNode = PseudoTreeNode(name, nodesAndNeighbours[name],
                                  var=self.variable_x_unary_constraint[name],
                                  parent=parent_node)
        self._AppendNodeToPseudoTree(rootNode)
        return rootNode

    def _AppendNodeToPseudoTree(self, ptn):
        if ptn not in self.PseudoNodes:
            self.PseudoNodes.append(ptn)

    def ExportGraph(self, number_of_agents):
        with open(".\\extra\\MSP_" + str(number_of_agents) + "_PseudoTree.txt", "w") as f:
            f.write("digraph G { " + '\n')
            for node in self.PseudoNodes:
                for child in node.get_Child():
                    f.write('"' + node.name + '" -> ' + '"' + child.name + '"' + ';' + '\n')
                for pseudo_child in node.get_PseudoChild():
                    f.write('"' + node.name + '" -> ' + '"' + pseudo_child.name + '"' + " [style = dashed]" + ';' + '\n')
            f.write("}")


    def compute_node_seperators(self):
        for node in PostOrderIter(self.root):
            if node.is_leaf:
                node._SEP = node._SEP + node.get_Parent() + node.get_PseudoParent()
            else:
                node._SEP = node._SEP + node.get_Parent() + node.get_PseudoParent()
                for child in node.children:
                    node._SEP = node._SEP + child._SEP

            # remove duplicates
            node._SEP = list(dict.fromkeys(node._SEP))

            if node in node._SEP:
                node._SEP.remove(node)

    def print_node_seperators(self):
        print("-----------------------------------")
        print("Printing Node Separators")
        print("-----------------------------------")
        for node in PostOrderIter(self.root):
            print("Separators for node " + node.name)
            for item in node._SEP:
                print(item.name)

                a, b = item.compute_binary_constraint(node)
                print(a)
                print(b)



class PseudoTreeNode(NodeMixin):

    def __init__(self, name,  neighbours, var,  parent=None, children=None):
        super(PseudoTreeNode, self).__init__()
        self.name = name
        self._P = []
        self._PP = []
        self._C = []
        self._PC = []
        self._SEP = []
        self.var = var
        self.Neighbours = neighbours
        self.parent = parent

        if children:
            self.children = children

    def set_Parent(self, x):
        if not x in self._P:
            self._P.append(x)

    def get_Parent(self):
        return self._P

    def set_Seperator(self, x):
        if not x in self._SEP:
            self._SEP.append(x)

    def get_Seperator(self):
        return self._SEP

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


    def compute_binary_constraint(self, v2):



        binary_constraint = np.zeros(shape=(len(self.var.domain), len(self.var.domain)))

        v1_agent = self.name.split("_")[0]
        v1_meeting = self.name.split("_")[1]
        v2_agent = v2.name.split("_")[0]
        v2_meeting = v2.name.split("_")[1]


        if v1_agent == v2_agent:
            if v1_meeting != v2_meeting:
                for i in range(len(self.var.utils)):
                    for j in range(len(v2.var.utils)):
                        if i == j:
                            binary_constraint[i][j] = 0
                        else:
                            binary_constraint[i][j] = int(self.var.utils[i]) + int(v2.var.utils[i])

        elif v1_meeting == v2_meeting:
            if v1_agent != v2_agent:
                for i in range(len(self.var.utils)):
                    for j in range(len(v2.var.utils)):
                        if i == j:
                            binary_constraint[i][j] = int(self.var.utils[i]) + int(v2.var.utils[i])
                        else:
                            binary_constraint[i][j] = 0


        return [self.name, v2.name], binary_constraint