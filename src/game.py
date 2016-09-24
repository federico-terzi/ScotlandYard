'''
Created on 07/set/2016

@author: Lorenzo Selvatici
'''

from agents import AgentRole
from rules import Rules
from settings import Settings



class GameStateData:
    """
    Store all the data of a game state (GameState). 
    It will be passed to the graphic object to initialize/update the GUI.
    """
    
    def __init__(self, layout, agents):
        """
        Initialize the data of a game state: layout (see Layout.py), a list of agent (Agent in agents.py)
        Mr. X in the agent at index 0. The remainder are the cops.
        """
        assert len(agents)>=2, "Too few agents!"
        self.layout = layout
        self.agents = agents
    
    def getNumMoves(self):
        """
        Returns the number of Mr.X moves.
        """
        return len(self.getAgentState(0).getMovesHistory())
    
    def getAgent(self, agentIndex):
        """
        Returns the agent at index agentIndex in self.agents.
        Mr. X in the agent at index 0. The remainder are the cops.
        """
        assert 0 <= agentIndex < len(self.agents)
        return self.agents[agentIndex]
        
    def getAgentState(self, agentIndex):
        """
        Returns the state of the agent at index agentIndex in self.agents.
        Mr. X in the agent at index 0. The remainder are the cops.
        """
        return self.getAgent(agentIndex).getAgentState()
    
    def numberOfCops(self):
        """
        Returns the number of cops.
        """
        return len(self.agents) - 1
    
    def deepCopy(self):
        """
        Returns a copy of the Game State Data.
        """
        agents_copy = [a.deepCopy() for a in self.agents]
        return GameStateData(self.layout, agents_copy)
    
    def __eq__(self, other):
        return self.agents==other.agents and self.layout==other.layout
    
    def __str__(self):
        return "\n\n".join([a.__repr__() for a in self.agents])

class GameState:
    """
    A wrapper for GameStateData.
    Modules outside of game.py should use it as the only way to collect information of the state of the game.
    """
    def __init__(self, data):
        """
        Initializes the game state with the supplied instance of GameStateData.
        """
        self.data = data
    
    def getNumMoves(self):
        """
        Returns the number of Mr.X moves.
        """
        return len(self.data.getAgentState(0).getMovesHistory())
    
#     def getLegalPositions(self):
#         """
#         Returns the list of legal positions.
#         """
#         return self.data.layout.getNodesStations().keys()
    
    def deepCopy(self):
        """
        Returns a copy of itself.
        """
        return GameState(self.data.deepCopy())
    
    def getCopPosition(self, copIndex = None):
        """
        Returns the position of the cop at the specified index.
        The index should be an integer in the interval [1, numberOfCops].
        """
        if copIndex is not None:
            return self.data.getAgentState(copIndex).getPosition()
        else:
            return [self.getCopPosition(i+1) for i in range(self.numberOfCops())]
    
    def getCopState(self, copIndex):
        """
        Returns the state of the cop at the specified index.
        The index should be an integer in the interval [1, numberOfCops].
        """
        return self.data.getAgentState(copIndex)
    
    def numberOfCops(self):
        """
        Returns the number of cops.
        """
        return self.data.numberOfCops()

    def getLegalCopActions(self, copIndex):
        """
        Returns the list of the legal actions of the cop at the specified index.
        The index should be an integer in the interval [1, numberOfCops].
        """
        return Rules.getLegalActions(self.data.getAgent(copIndex), self.data)
     
    def getMrXEvidences(self):
        """
        Returns the evidences collected up to this point and the positions where Mr.X was seen.
        """
        not_hidden_moves = self.data.agents[0].notHiddenMoves
        moves_history = self.data.agents[0].getAgentState().getMovesHistory()
        ticket_history = [action.getTicketType() for action in moves_history]
        print "\n\n" + "="*30
        print self
        print "\n" + str(not_hidden_moves) + "\n" + "="*30
        return ticket_history, not_hidden_moves 
          
    
    def generateSuccessor(self, agentIndex, action):
        """
        Returns a new instance of GameState where the agent at the specified agentIndex has taken his action.
        AgentIndex is an integer in the interval [0, numberOfCops]. Index 0 is Mr. X.
        """
        # assert it's not a final state
        turn = AgentRole.Mr_X if agentIndex==0 else AgentRole.COP
        assert not self.isEndState(turn)[0] # check the first boolean element of the tuple
        
        new_state = self.deepCopy()
        agent = new_state.data.getAgent(agentIndex)
        if not Rules.isLegalAction(agent, action, self.data):
            raise Exception("Illegal action!" + action.__str__())
        
        agent.performAction(action)
        return new_state
    
    def isEndState(self, turn):
        """
        Returns a tuple of 3 elements.
        (True, AgentRole, String) if the game is over, AgentRole is the winner and String is a description of the state.
        (False, None, "") if the game is NOT over.
        
        The input parameter turn (AgentRole) determines whose turn.
        """
        # check for an overlap between Mr.X position and the cops' ones
        mrXposition = self._getMrXPosition()
        copPositions = self.getCopPosition()
        if mrXposition in copPositions:
            return (True, AgentRole.COP, "Mr. X has been caught from COP n." + \
                    str(copPositions.index(mrXposition)+1) + ".\nThe winners are the COPS.\n")
        
        # check if the the maximum number of moves have been reached
        if self.getNumMoves() == Settings.getMaxNumMoves() and turn == AgentRole.Mr_X:
            return (True, AgentRole.Mr_X, "Maximum number of moves reached (" + str(Settings.getMaxNumMoves()) + \
                    ").\nThe winner is Mr. X.\n")
        
        # check if Mr.X has no legal moves available
        if len(self._getLegalMrXActions())==0 and turn == AgentRole.Mr_X:
            return (True, AgentRole.COP, "Mr. X can not move from his position " + \
                    str(mrXposition) + ".\nThe winners are the COPS.\n")
              
        # check if the cops have run out of tickets (legalMoves)
        if turn == AgentRole.COP:
            for i in range(self.numberOfCops()):
                if self.getLegalCopActions(i+1) != []:
                    return (False, None, "")
            return (True, AgentRole.Mr_X, "The cops can not move.\nThe winner is Mr. X.\n")
        
        return (False, None, "")
    
    def _getMrXPosition(self):
        return self.data.getAgentState(0).getPosition()
    
    def _getLegalMrXActions(self):
        return Rules.getLegalActions(self.data.getAgent(0), self.data)
    
    def __eq__(self, other):
        return self.data == other.data
        
    def __repr__(self):
        return self.data.__str__()    
        
if __name__ == '__main__':
    from agents import  MrX, KeyboardMrX, KeyboardCop, Cop
    agents_list = [KeyboardMrX()] + [KeyboardCop(i+1) for i in range(Settings.getNumberOfCops())]
    layout = Settings.getLayout()
    data = GameStateData(layout, agents_list)
    
    gameState = GameState(data)
    print gameState
    print "="*30
    turn = AgentRole.Mr_X
    counter=0
    while gameState.isEndState(turn)[0]==False:
        gameState = gameState.generateSuccessor(counter, gameState.data.getAgent(counter).getAction(gameState))
        print "="*20
        print gameState
        print "="*30
        counter+=1
        counter = counter % len(agents_list)
        turn = AgentRole.Mr_X if counter==0 else AgentRole.COP









