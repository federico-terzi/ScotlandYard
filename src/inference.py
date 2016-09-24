'''
Created on 23/set/2016

@author: Lorenzo Selvatici
'''
import util
import rules
from settings import Settings

def distributionFrom(old_pos, ticket_used, gameState):
    """
    Returns a distribution which stores the probabilities of being in a position, given the previous
    position the ticket_used used and the current gameState.
    """
    def getWeight(end, gameState):
        cops_pos = gameState.getCopPosition()
        if end in cops_pos:
            return 0
        # IMPROVEMENT: consider the positions of the cops
        return 1
    
    result = util.Counter()
    
    edges = Settings.getLayout().getEdgesFromNode(old_pos)  # (int, int, EdgeType, [])
    
    if ticket_used == rules.TicketType.BLACK:
        # all edges are possible
        ends = [edge[1] for edge in edges]
        for end in ends:
            result[end] = getWeight(end, gameState)
        result.normalize()
        return result
        
    # else   
    for edge in edges:
        start, end, edge_ticket, _ = edge
        assert start == old_pos and end!=start
        if ticket_used == edge_ticket:
            result[end] = getWeight(end, gameState)
    
    result.normalize()
    return result
        
        


class ExactInference:
    """
    The exact dynamic inference module uses forward-algorithm updates to
    compute the exact belief function at each time step.
    """
    def __init__(self, beliefs = None):
        """
        Initializes the belief distribution uniformly.
        """
        self.nextMoveToObserve = 0
        
        if beliefs is None:     
            self.beliefs = util.Counter()
            for pos in Settings.getLegalPositions():
                self.beliefs[pos] = 1
            self.beliefs.normalize()
        else:
            self.beliefs = beliefs
        
        
    def deepCopy(self):
        return ExactInference(self.beliefs.copy())
    
    
    def updateBeliefs(self, ticketList, notHiddenMoves, gameState):
        """
        Updates the beliefs distribution according to the new evidences.
        ticketList is the list of the tickets used by Mr.X
        notHiddenMoves is a dictionary in the format { numberOfMove : position }
        """
        assert len(ticketList) == (self.nextMoveToObserve + 1), \
                (len(ticketList), self.nextMoveToObserve + 1)
        
        if self.nextMoveToObserve+1 in notHiddenMoves:
            self.beliefs = util.Counter()
            mrxPos = notHiddenMoves[self.nextMoveToObserve+1]
            self.beliefs[mrxPos]=1  # we are sure about the position of Mr.X
        else:
            new_beliefs = util.Counter()
            
            ticket = ticketList[self.nextMoveToObserve]
            for old_pos in self.beliefs.keys():
                new_pos_dist = distributionFrom(old_pos, ticket, gameState)
                for new_pos, prob in new_pos_dist.items():
                    new_beliefs[new_pos] += self.beliefs[old_pos] * prob

            new_beliefs.normalize()
            self.beliefs = new_beliefs
        
        self.nextMoveToObserve += 1
            
            
    def getBeliefsDistribution(self):
        """
        Returns the current beliefs distribution.
        """
        return self.beliefs
    

if __name__ == "__main__":
    ei = ExactInference()
    # print ei.getBeliefsDistribution()
    ei.updateBeliefs(["TAXI"], {}, None)
    bd = ei.getBeliefsDistribution()
    print bd
    print bd.argMax()
    
    
    
    
    
    
    
    