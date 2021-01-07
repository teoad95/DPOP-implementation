import unittest
from GraphClass import Graph

class GraphTests(unittest.TestCase):

    def test_GraphCreation(self):
        #Assume
        g = {"a": ["c"],
             "b": ["c", "e"],
             "c": ["a", "b", "d", "e"],
             "d": ["c"],
             "e": ["c", "b"],
             "f": []
             }
        graph = Graph(g)

        #Assert
        self.assertTrue(graph.vertices() == "['a', 'b', 'c', 'd', 'e', 'f']")
        self.assertTrue(graph.edges() == "[{'a', 'c'}, {'b', 'c'}, {'e', 'b'}, {'d', 'c'}, {'e', 'c'}]")