import random
from GraphClass import Graph
from PseudoTreeClass import PseudoTree

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


class MspSolver(object):

    def __init__(self):
        self.numOfAgents = None
        self.numOfMeetings = None
        self.numOfVariables = None

        self.agents = []
        self.meetings = []
        self.variables = {}
        self.problem_graph = Graph({})
        self.pseudo_tree = None

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
                    #print("Creating Agent " + agentId)
                    createdAgents.append(agentId)
                    self.agents.append(Agent('A'+agentId))

                if meetingId not in createdMeetings:
                    #print("Creating Meeting " + meetingId)
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

                for j in range(8):
                    line = reader.readline()
                    lineToList = line.strip('\n').split(',')
                    utils.append(lineToList[2])

                for agent in self.agents:
                    if agent.name == ('A'+str(i)):
                        agent.time_utils = utils

            # print(self.variables)
            # for agent in self.agents:
            #     print(agent.name)
            #     print(agent.time_utils)
            #     for meeting in agent.meetings:
            #         print(meeting.mid)
            #         print(meeting.participants)
            #     print("-------------------------------")
            #
            # for meeting in self.meetings:
            #     print(meeting.mid)
            #     print(meeting.participants)
            #     print("-------------------------------")
            #     #print(line, end='')
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

         with open(".\\extra\\MSP_Problem_Graph_" + str(self.numOfAgents) + ".txt", "w") as f:
            f.write("graph G { " + '\n')

            for i in self.variables:
                f.write(i + '\n')

            f.write('\n')
            for agent in self.agents:
                constraints = []
                for meeting in agent.meetings:
                    constraints.append(agent.name + '_' + meeting.mid)
                    # print(agent.name+'_'+meeting.mid )
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


         with open(".\\extra\\MSP_Problem_Graph_nocolor_" + str(self.numOfAgents) + ".txt", "w") as f:
            f.write("graph G { " + '\n')

            for vertex in self.problem_graph.vertices():
                f.write(vertex + '\n')

            f.write('\n')

            _problem_graph_dict = self.problem_graph.getNodesAndNeighbours()

            for vertex in _problem_graph_dict:
                for item in _problem_graph_dict[vertex]:
                    f.write(vertex + '--' + item+ '\n')

            f.write("}")

    def create_pseudo_tree(self):

        tree = PseudoTree(self.problem_graph)
        random_root = random.choice(self.problem_graph.vertices())
        print("...Choosing random root " + random_root)
        root_node = tree.CreateNodeAndAddItOnTree(random_root)
        tree.PseudoTreeNodesCreation(root_node)
        tree.ExportGraph()

if __name__ == "__main__":

    MspSolver = MspSolver()
    MspSolver.load_problem('.\\extra\\MSP_Problem_5.txt')
    MspSolver.create_graph()
    MspSolver.export_graph()
    MspSolver.create_pseudo_tree()




