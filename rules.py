'''
Created on 09/set/2016

@author: Lorenzo Selvatici
'''

# from layout import EdgeType

class Rules:
    """
    Represents the rules of Scotland Yard.
    """
    
    def getLegalActions(agent, gameStateData):
        """
        Returns the list of possible actions (Action) for the specified agent (Agent), given the game state data (GameStateData). 
        """
        actions = []
        agentState = agent.getAgentState()
        agentPosition = agentState.getPosition()
        tickets = agentState.getTicketsAsDict()
        edges = gameStateData.layout.getEdgesFromNode(agentPosition) # list of tuples: (agentPosition, end, edgeType, path)
        
        for start, end, edge_type, _ in edges:
            assert start == agentPosition
            
            # the BLACK ticket can be used for all of the types of edges
            # the only way to travel on a FERRY edge type is to use a BLACK ticket
            if "BLACK" in tickets and tickets["BLACK"]>0: 
                actions.append(Action(start, end, TicketType.BLACK))
            
            #if edge_type == EdgeType.FERRY: # already checked! the only way to take a ferry is by using a BLACK ticket
            #    continue
            
            # edge_type is one of the following : TAXI, BUS, UNDERGROUND
            if edge_type in tickets and tickets[edge_type] > 0:
                actions.append(Action(start, end, edge_type))
         
        # filter the actions, deleting the ones with endState equals to the position of a cop
        copPositions = [gameStateData.getAgentState(i + 1).getPosition() for i in range(gameStateData.numberOfCops())]
        filtered_actions = filter(lambda action: action.getEnd() not in copPositions, actions)
        return filtered_actions
               
    getLegalActions = staticmethod(getLegalActions)
    
    def isLegalAction(agent, action, gameStateData):
        """
        Returns True if the action is legal, False otherwise.
        """
        return action in Rules.getLegalActions(agent, gameStateData)
    
    isLegalAction = staticmethod(isLegalAction)
    
    def getRandomNode(gameStateData):
        """
        Returns a random LEGAL node in the interval [1, numNodes], given a GameStateData.
        A legal node is a node not occupied by a cop.
        If a Mr. X agent calls this function, it must call it as below:
        
        new_pos = Rules.getRandomNode(currentGameStateData)
        while new_pos==old_pos:
            new_pos = Rules.getRandomNode(currentGameStateData)
        # now new_pos is a legal position for Mr.X
        
        """
        cop_positions = [gameStateData.getAgentState(i+1).getPosition() for i in range(gameStateData.numberOfCops())]
        
        import random
        new_pos = random.choice(range(gameStateData.layout.getNumNodes())) + 1
        while new_pos in cop_positions:
            new_pos = random.choice(range(gameStateData.layout.getNumNodes())) + 1
        return new_pos 
    
    getRandomNode = staticmethod(getRandomNode)
    


class TicketType:
    """
    Enumeration representing the possible types of Ticket.
     
    """
    TAXI = "TAXI"
    BUS = "BUS"
    UNDERGROUND = "UNDERGROUND"
    BLACK = "BLACK" # a hidden ticket, only Mr. X can use it. 
    # It's the only ticket which can be used for the FERRY edges. 
    # You may want to use it for hiding your movements (it can be used as taxi, bus or underground ticket as well)
     
    def asList():
        """
        Return all the possible types of edge.
        """
        return [TicketType.TAXI, TicketType.BUS, TicketType.UNDERGROUND, TicketType.BLACK]
    asList = staticmethod(asList)


class Action:
    """
    Represents an action as a tuple: (startNode, endNode, ticketType) - (int, int, TicketType)
    """
    
    def __init__(self, start, end, ticket):
        assert start!=end
        self.start=start
        self.end=end
        self.ticket=ticket
    
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
    
    def getTicketType(self):
        return self.ticket
    
    def __eq__(self, other):
        return self.start==other.start and self.end==other.end and self.ticket==other.ticket
    
    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        return str(self.start) + " -> " + str(self.end) + " " + self.ticket


if __name__ == '__main__':
    # action tests
#     a = Action(1, 2, "A")
#     b = Action(1, 2, "A")
#     assert a == b
#     print "passed!"
    
    # rules tests
    pass






