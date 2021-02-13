import random
from GraphClass import Graph
from PseudoTreeClass import PseudoTree
from DPOPClass import Dpop


DOMAIN = ["8", "9", "10", "11", "12", "13", "14", "15"]
#DOMAIN = ["8", "9", "10" ]

class Agent:

    # instance attributes
    def __init__(self, name):
        self.name = name
        self.time_utils = []
        self.meetings = []


class Meeting:

    def __init__(self, mid, participants):
        self.mid = mid
        self.participants = participants


class Variable:
    def __init__(self, name, domain, utils):
        self.name = name
        self.domain = domain
        self.utils = utils
        self.optimal_value = "N/A"


class MspSolver(object):

    def __init__(self):
        self.numOfAgents = None
        self.numOfMeetings = None
        self.numOfVariables = None
        self.PseudoTrees = []
        self.agents = []
        self.meetings = []
        self.variables = {}
        self.problem_graph = Graph({})
        self.variable_x_unary_constraint = {}

    def load_problem(self, filename):

        with open(filename, 'r') as reader:

            line = reader.readline()

            # Read First Line
            lineToList = line.strip('\n').split(',')

            self.numOfAgents = int(lineToList[0])
            self.numOfMeetings = int(lineToList[1])
            self.numOfVariables = int(lineToList[2])

            createdAgents = []
            createdMeetings = []
            for i in range(self.numOfVariables):
                line = reader.readline()
                lineToList = line.strip('\n').split(',')

                agentId = lineToList[0]
                meetingId = lineToList[1]
                meetingUtil = lineToList[2]

                if agentId not in createdAgents:
                    createdAgents.append(agentId)
                    self.agents.append(Agent('A'+agentId))

                if meetingId not in createdMeetings:
                    createdMeetings.append(meetingId)
                    self.meetings.append(Meeting('M'+meetingId, {}))

                for meeting in self.meetings:
                    if meeting.mid == ('M'+meetingId):
                        currentMeetingObject = meeting
                        meeting.participants['A'+agentId] = meetingUtil

                self.variables['A'+agentId+'_M'+meetingId] = meetingUtil

                for agent in self.agents:
                    if agent.name == ('A'+agentId):
                        meetingNames = []
                        for meeting in agent.meetings:
                            meetingNames.append(meeting.mid)
                        if 'M'+meetingId not in meetingNames:
                            agent.meetings.append(currentMeetingObject)



            for i in range(1, self.numOfAgents+1):
                utils = []

                for j in range(len(DOMAIN)):
                    line = reader.readline()
                    lineToList = line.strip('\n').split(',')
                    utils.append(lineToList[2])

                for agent in self.agents:
                    if agent.name == ('A'+str(i)):
                        agent.time_utils = utils

            self.variable_x_unary_constraint = self.compute_unary_constraints()

            print("-------------------------------")
            print("DCOP Problem Description")
            print("-------------------------------")
            print("Number of Agents: " + str(self.numOfAgents))
            print("Number of Meetings: " + str(self.numOfMeetings))
            print("Number of Variables: " + str(self.numOfVariables))

    def create_graph(self):

        for var in self.variables:
            self.problem_graph.add_vertex(var)

        for agent in self.agents:
            constraints = []
            for meeting in agent.meetings:
                constraints.append(agent.name + '_' + meeting.mid)
            M = len(constraints)
            for c in range(M):
                k = constraints.pop()
                for j in constraints:
                    self.problem_graph.add_edge({k, j})

        for meeting in self.meetings:
            constraints = []
            for p in meeting.participants:
                constraints.append(p + '_' + meeting.mid)

            M = len(constraints)
            for c in range(M):
                k = constraints.pop()

                for j in constraints:
                    self.problem_graph.add_edge({k, j})

    def export_graph(self):

         with open(".\\extra\\MSP_" + str(self.numOfAgents) + "_Problem_Graph.txt", "w") as f:
            f.write("graph G { " + '\n')

            for i in self.variables:
                f.write(i + '\n')

            f.write('\n')
            for agent in self.agents:
                constraints = []
                for meeting in agent.meetings:
                    constraints.append(agent.name + '_' + meeting.mid)
                M = len(constraints)
                for c in range(M):

                    k = constraints.pop()

                    for j in constraints:
                        f.write(k + ' -- ' + j + '  [style = bold, color = red]' + '\n')

            for meeting in self.meetings:
                constraints = []
                for p in meeting.participants:
                    constraints.append(p + '_' + meeting.mid)

                M = len(constraints)
                for c in range(M):
                    k = constraints.pop()

                    for j in constraints:
                        f.write(k + ' -- ' + j + '  [style = bold, color = darkgreen]' + '\n')

            f.write("}")

         with open(".\\extra\\MSP_" + str(self.numOfAgents) + "_Problem_Graph_nocolor.txt", "w") as f:
            f.write("graph G { " + '\n')

            for vertex in self.problem_graph.vertices():
                f.write(vertex + '\n')

            f.write('\n')

            _problem_graph_dict = self.problem_graph.getNodesAndNeighbours()

            for vertex in _problem_graph_dict:
                for item in _problem_graph_dict[vertex]:
                    f.write(vertex + '--' + item+ '\n')

            f.write("}")

    def create_pseudo_tree(self, rootNode = ""):
        graph = self.problem_graph
        while True:
            tree = PseudoTree(graph, self.variable_x_unary_constraint)
            tree.PseudoTreeCreation(rootNode)
            tree.ExportGraph(self.numOfAgents)
            self.PseudoTrees.pop(tree)
            if not any(tree.NodesNotIncludedInTree):
                break
            graph = tree.NodesNotIncludedInTree



    def compute_unary_constraints(self):

        variable_x_unary_constraint = {}

        for v in self.variables:
            agent_name = v.split("_")[0]

            for a in self.agents:
                if a.name == agent_name:
                    unary_constraint = []

                    for i in range(len(a.time_utils)):
                        unary_constraint.append(int(a.time_utils[i]) * int(self.variables[v]))
                        variable = Variable(v, DOMAIN, unary_constraint)
                        variable_x_unary_constraint[v] = variable


        return variable_x_unary_constraint



if __name__ == "__main__":

    MspSolver = MspSolver()
    MspSolver.load_problem('.\\extra\\MSP_20_Problem.txt')
    MspSolver.create_graph()
    MspSolver.export_graph()
    MspSolver.create_pseudo_tree()
    # MspSolver.pseudo_tree.showconstaints()
    # MspSolver.pseudo_tree.print_node_seperators()

    for tree in MspSolver.PseudoTrees:
        algorithm = Dpop(tree)
        algorithm.Solve_Problem()






