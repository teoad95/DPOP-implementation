import random
import graph

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


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

    def export_graph(self):

        with open(".\\extra\\MSP_Problem_Graph" + str(self.numOfAgents) + ".txt", "w") as f:
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


if __name__ == "__main__":
    g = {"a": ["d"],
         "b": ["c"],
         "c": ["b", "c", "d", "e"],
         "d": ["a", "c"],
         "e": ["c"],
         "f": []
         }

    graph = Graph(g)
    MspSolver = MspSolver()
    MspSolver.load_problem('.\\extra\\MSP_Problem_5 .txt')
    MspSolver.export_graph()

    print("Add an edge:")
    graph.add_edge({"a", "z"})

    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())


