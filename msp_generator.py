from anytree import NodeMixin, LevelOrderIter, PreOrderIter
from anytree.exporter import DotExporter
import random
import sys

TIME_SLOT_UTIL = [[10, 20, 30, 40, 50, 60, 70, 80],
                  [80, 70, 60, 50, 40, 30, 20, 10],
                  [10, 10, 10, 10, 10, 10, 10, 10]]

MEETING_UTIL = ['100', '70', '50', '30', '10']

MAX_MEETINGS = 8

TOTAL_MEETINGS = 0


class Meeting:
    """
    A Meeting object.

    Attributes:
        mid (int): The meeting unique ID
        participants (dict): Stores {participant:utility value}
        type (str): The meeting type
    """

    def __init__(self, mid, participants, type):
        """
          The constructor for Meeting class.

          Parameters:
            mid (int): The meeting unique ID
            participants (dict): Stores {participant:utility value}
            type (str): The meeting type
        """
        self.mid = mid
        self.participants = participants
        self.type = type


class Agent:
    """
    An Agent object.

    Attributes:
        time_utils (list[int]): The agent's time utilities
        meetings (list[Meeting]): A list of the scheduled Meetings
    """

    def __init__(self):
        """
          The constructor for Meeting class.
        """
        self.time_utils = random.choice(TIME_SLOT_UTIL)
        self.meetings = []


class AgentNode(Agent, NodeMixin):
    """
    An AgentNode object. Extends NodeMixin class from anytree
    module.

    Attributes:
        name (str): The agent name
        parent (AgentNode): The parent node
        children (AgentNode): The node's children
    """
    def __init__(self, name, parent=None, children=None):
        """
          The constructor for Meeting class.

          Parameters:
            name (str): The agent name
            parent (AgentNode): The parent node
            children (AgentNode): The node's children
        """
        super(AgentNode, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def create_grp(self):
        global TOTAL_MEETINGS

        agentChildren = list(self.children)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentChildren) > 0:
                for item in agentChildren + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentChildren + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "GRP")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1
                return True
            else:
                return False
        else:
            return False

    def create_sib(self):
        global TOTAL_MEETINGS

        agentSiblings = list(self.siblings)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentSiblings) > 0:
                numberOfParticipants = random.randint(1, len(agentSiblings))

                if numberOfParticipants > 3:
                    numberOfParticipants = random.randint(1, 3)

                # Choose a random subset of agent siblings
                agentSiblings = random.sample(agentSiblings, numberOfParticipants)

                for item in agentSiblings + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentSiblings + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "SIB")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1
                return True
            else:
                return False
        else:
            return False

    def create_ptc(self):
        global TOTAL_MEETINGS

        agentChildren = list(self.children)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentChildren) > 0:
                numberOfParticipants = random.randint(1, len(agentChildren))

                if numberOfParticipants > 3:
                    numberOfParticipants = random.randint(1, 3)

                # Choose a random subset of agent children
                agentChildren = random.sample(agentChildren, numberOfParticipants)

                for item in agentChildren + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentChildren + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "PTC")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1
                return True

            else:
                return False
        else:
            return False


class AgentHierarchy:
    def __init__(self, num_of_agents):
        self.numOfAgents = num_of_agents
        self.root = None

    def create_hierarchy(self):

        totalAgents = self.numOfAgents

        agentNum = 1
        level = 1
        nodeName = "A" + str(agentNum)
        root = AgentNode(nodeName)
        agentNum += 1
        currentParent = root
        availableNodes = []
        availableNodesInner = []

        while agentNum <= totalAgents:

            nodeName = "A" + str(agentNum)

            if len(currentParent.children) < level + 1:
                currentNode = AgentNode(nodeName, parent=currentParent)
                availableNodes.append(currentNode)
                agentNum += 1

            else:

                level += 1
                N = len(availableNodes)

                while (N > 0) & (agentNum <= totalAgents):

                    nodeName = "A" + str(agentNum)
                    currentParent = availableNodes[0]

                    if len(currentParent.children) < level + 1:
                        currentNode = AgentNode(nodeName, parent=currentParent)
                        availableNodesInner.append(currentNode)
                        agentNum += 1

                    else:
                        currentParent = availableNodes.pop(0)
                        N -= 1

                availableNodes = availableNodesInner

        DotExporter(root).to_dotfile(".\\extra\\MSP_"+str(self.numOfAgents)+"_Hierarchy_Tree.dot")

        self.root = root

    def create_meeting_bfs(self):
        for agent in [node for node in LevelOrderIter(self.root)]:

            meeting_type = random.randint(1, 20)

            if meeting_type < 10:
                agent.create_grp()
            elif meeting_type < 20:
                agent.create_ptc()
            elif meeting_type >= 19:
                agent.create_sib()

    def create_meeting_dfs(self):
        for agent in [node for node in PreOrderIter(self.root)]:

            meeting_type = random.randint(1, 22)

            if meeting_type < 10:
                agent.create_grp()
            elif meeting_type < 20:
                agent.create_ptc()
            elif meeting_type >= 20:
                agent.create_sib()

    def generate_missing_meetings(self):

        for agent in [node for node in LevelOrderIter(self.root)]:

            if len(agent.meetings) == 0:

                if agent.create_grp():
                    pass
                elif agent.create_ptc():
                    pass
                elif agent.create_sib():
                    pass

    def print_generator_output_detail(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)
        print("NumberOfAgents;TotalMeetings;TotalVariables")
        print(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables))

        print("AgentNumber;MeetingID;Utility")
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                print(agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name])

        print("AgentNumber;TimeSlot;TimeSlotUtility")
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.time_utils:
                print(agent.name.replace('A', '') + "," + str(agent.time_utils.index(item) + 1) + "," + str(item))

    def print_generator_output(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)

        print(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables))

        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                print(agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name])

        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.time_utils:
                print(agent.name.replace('A', '') + "," + str(agent.time_utils.index(item) + 1) + "," + str(item))

    def print_statistics(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)
        print("-----------------------------")
        print("Number of Agents: " + str(self.numOfAgents))
        print("Number of Meetings: " + str(TOTAL_MEETINGS))
        print("Number of Variables: " + str(numOfVariables))

        print("-----------------------------")

        cntGRP = 0
        cntPTC = 0
        cntSIB = 0

        meetingList = []
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                if item.mid not in meetingList:
                    meetingList.append(item.mid)
                    if item.type == 'GRP':
                        cntGRP += 1
                    elif item.type == 'PTC':
                        cntPTC += 1
                    elif item.type == 'SIB':
                        cntSIB += 1

        print("GRP: " + str(cntGRP))
        print("PTC: " + str(cntPTC))
        print("SIB: " + str(cntSIB))

        agentsNoMeeting = 0
        for agent in [node for node in LevelOrderIter(self.root)]:

            if len(agent.meetings) == 0:
                agentsNoMeeting += 1

        print("Agents with no meetings: " + str(agentsNoMeeting))

    def export_to_file(self):

        with open(".\\extra\\MSP_"+str(self.numOfAgents)+"_Problem.txt", "w") as f:

            numOfVariables = 0

            for agent in [node for node in LevelOrderIter(self.root)]:
                numOfVariables += len(agent.meetings)

            f.write(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables) + '\n')

            for agent in [node for node in LevelOrderIter(self.root)]:

                for item in agent.meetings:
                    f.write(
                        agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name] + '\n')

            for agent in [node for node in LevelOrderIter(self.root)]:

                counter = 1
                for item in agent.time_utils:
                    f.write(agent.name.replace('A', '') + "," + str(counter) + "," + str(item) + '\n')
                    counter += 1


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Provide the number of agents(example: python msp_generator.py 50)")
        sys.exit()
    val = sys.argv[1]

    try:
        N = int(val)
        print("Generating Meeting Scheduling Problem")
    except ValueError:
        print("Provide Number!")
        sys.exit()

    H = AgentHierarchy(N)
    H.create_hierarchy()
    # H.create_meeting_bfs()
    H.create_meeting_dfs()
    H.generate_missing_meetings()
    H.export_to_file()
    H.print_statistics()
