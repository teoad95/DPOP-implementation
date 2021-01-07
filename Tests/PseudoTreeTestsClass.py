import unittest
from GraphClass import Graph
from PseudoTreeClass import PseudoTree, Token

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

    def test_TreeConstruction(self):
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
        root_node = tree.CreateNodeAndAddItOnTree("X0")
        token = Token("X0")
        tree.PseudoTreeNodesCreation(root_node, token)
        # Assert
        self.assertCountEqual(tree.PseudoNodes, 5)
        # TODO Add validations for each Pseudonode P, PP, C, PC