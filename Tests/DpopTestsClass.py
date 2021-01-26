import unittest
from msp_solver import MspSolver
from DPOPClass import Dpop


class DpopTests(unittest.TestCase):

    def test_readFile(self):
        # PrepareData
        Solver = MspSolver()
        # Solver.load_problem('.\\extra\\MSP_4_PseudoTree.txt')
        Solver.load_problem('.\\extra\\simpleMeetingTestWith4Agents.txt')
        Solver.create_graph()
        Solver.create_pseudo_tree("A1_M1")
        Solver.pseudo_tree.print_node_seperators()
        algorithm = Dpop(Solver.pseudo_tree)

        A4_M2 = [e for e in Solver.pseudo_tree.PseudoNodes if e.name == "A4_M2"]
        utilFromA4M2ToA1M2 = algorithm.CalculateUtil(A4_M2.pop(0))
        self.assertEqual(len(utilFromA4M2ToA1M2.dimensions()), 1)

        A2_M1 = [e for e in Solver.pseudo_tree.PseudoNodes if e.name == "A2_M1"]
        utilFromA2M1ToA3M1 = algorithm.CalculateUtil(A2_M1.pop(0))
        self.assertEqual(len(utilFromA2M1ToA3M1.dimensions()), 2)


    def test_readFile2(self):
        # PrepareData
        Solver = MspSolver()
        #Solver.load_problem('.\\extra\\MSP_3_Problem.txt')
        Solver.load_problem('.\\extra\\simpleMeetingTestWith4Agents.txt')
        Solver.create_graph()
        Solver.create_pseudo_tree()
        #Solver.pseudo_tree.print_node_seperators()
        algorithm = Dpop(Solver.pseudo_tree)
        algorithm.Solve_Problem()
