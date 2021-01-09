import unittest
from GraphClass import Graph
from PseudoTreeClass import PseudoTree
from anytree.exporter import DotExporter

class PseudoTreeTests(unittest.TestCase):

    def test_RootNodeElection(self):
        #Assume
        g = {"a": ["c"],
             "b": ["c", "e"],
             "c": ["a", "b", "d", "e"],
             "d": ["c"],
             "e": ["c", "b"],
             "f": []
             }
        graph = Graph(g)
        tree = PseudoTree(graph)

        #Action
        self.assertFalse(tree.PseudoNodes)
        tree.elect_root_node()

        #Assert
        self.assertTrue(tree.PseudoNodes)

    def test_TreeConstructionValidateNodes(self):
        # Assume
        g = {"X0": ["X1", "X4"],
                "X1": ["X0", "X4"],
                "X4": ["X0", "X1", "X9", "X10"],
                "X9": [],
                "X10": []
              }

        graph = Graph(g)
        tree = PseudoTree(graph)
        # Action
        # We will set ase root node X0
        root_node = tree.CreateNodeAndAddItOnTree("X0", parent_node=None)
        tree.PseudoTreeNodesCreation(root_node)
        # Assert
        # self.assertCountEqual(tree.PseudoNodes, 5)
        tree.ExportGraph(0)
        # TODO Add validations for each Pseudonode P, PP, C, PC

    def test_TreeConstruction_GenerateGraph(self):
        # Assume
        g = {"X0": ["X1", "X4", "X11", "X2"],
             "X1": ["X0", "X4", "X3", "X8"],
             "X4": ["X0", "X1", "X9", "X10"],
             "X9": ["X4"],
             "X10": ["X4"],
             "X3": ["X1", "X8", "X7"],
             "X8": ["X1", "X3"],
             "X7": ["X3"],
             "X11": ["X0", "X5"],
             "X5": ["X11", "X2", "X12"],
             "X2": ["X0", "X5", "X12", "X6"],
             "X12": ["X2", "X5"],
             "X6": ["X2", "X13"],
             "X13": ["X6"],
             }

        graph = Graph(g)
        tree = PseudoTree(graph)
        root_node = tree.CreateNodeAndAddItOnTree("X0", parent_node=None)
        tree.PseudoTreeNodesCreation(root_node)
        tree.ExportGraph(0)

        tree.root = root_node
        tree.compute_node_seperators()
        for node in tree.PseudoNodes:
                print("Seperators for node " + node.name)
                for item in node._SEP:
                    print(item.name)
        DotExporter(tree.root).to_dotfile(".\\extra\\MSP_0_Hierarchy_Tree.dot")
        # validate that the graph is the same as the books