import unittest
from GraphClass import Graph
from PseudoTreeClass import PseudoTree

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
        tree.PseudoTreeCreation()

        #Assert
        self.assertTrue(tree.PseudoNodes)