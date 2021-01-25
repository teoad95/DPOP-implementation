import unittest
from msp_solver import MspSolver
from DPOPClass import Dpop

class DpopTests(unittest.TestCase):

    def test_readFile(self):
        Solver = MspSolver()

        # Solver.load_problem('.\\extra\\MSP_4_PseudoTree.txt')
        Solver.load_problem('.\\extra\\simpleMeetingTestWith4Agents.txt')
        Solver.create_graph()
        Solver.create_pseudo_tree()
        Solver.pseudo_tree.print_node_seperators()
        algorithm = Dpop(Solver.pseudo_tree)
        algorithm.Solve_Proble()