'''
Created on 11/set/2016

@author: Lorenzo Selvatici
'''

import agents
import graphic.display
from agents import AgentRole
from game import GameState, GameStateData
from settings import Settings
import util


class Game:
    """
    The core of the application.
    """

    def __init__(self, layout, agents, display_class, turn=AgentRole.Mr_X):
        self.gameState = GameState(GameStateData(layout, agents))
        self.turn = turn
        # create a new <type>+Display object
        self.display = display_class(self.gameState.data)
        self.MOD = len(agents)  # number of players

    def run(self):
        """
        The main loop of the application.
        """
        self.display.start()
        counter = 0

        while self.gameState.isEndState(self.turn) == (False, None, ""):
            # ask for an action and create the new game state
            self.display.wait()
            
            new_action = self.gameState.data.getAgent(
                counter).getAction(self.gameState, self.display)

            if not new_action is None:  # if there is a possible action, do it
                self.gameState = self.gameState.generateSuccessor(
                    counter, new_action)
            else:
                self.display.wait()

            # update the display
            self.display.update(self.gameState.data)

            self.display.wait()
            # update the player turn
            counter += 1
            counter = counter % self.MOD
            self.turn = AgentRole.Mr_X if counter == 0 else AgentRole.COP

        # end of the main while loop
        self.display.showMessage(
            "GAME OVER\n\n" + self.gameState.isEndState(self.turn)[2])
        self.display.waitQuit()
        self.display.finish()


def createAgents():
    """
    Creates a list of agents according to the type of instances specified in the Settings.
    """
    mrx_type = Settings.getMrXType() + "MrX"
    cops_type = Settings.getCopsType() + "Cop"
    mrx = (agents.__dict__)[mrx_type]()
    cops = [(agents.__dict__)[cops_type](i + 1)
            for i in range(Settings.getNumberOfCops())]
    return [mrx] + cops


def createDisplay():
    """
    Creates the display according to the type specified in the Settings.
    """
    display_type = Settings.getDisplayType() + "Display"
    return (graphic.display.__dict__)[display_type]  # an object
# http://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package


if __name__ == '__main__':
    
    new_game = Game(Settings.getLayout(), createAgents(), createDisplay())
    new_game.run()
