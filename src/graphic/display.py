'''
Created on 12/set/2016

@author: Lorenzo Selvatici
'''

import util
import GUI_util as gu
import pygame
from settings import Settings
from agents import AgentRole


class Display:
    """
    A generic display.
    """

    def __init__(self, gameStateData):
        """
        Initializes a display given the data of a game state (GameStateData see game.py)
        """
        self.data = gameStateData

    def start(self):
        """
        Starts the display.
        """
        util.raiseNotDefined()

    def update(self, new_gameStateData):
        """
        Update the display with the new data supplied.
        """
        pass

    def wait(self, ms=None):
        """
        Wait for a user event.
        """
        util.raiseNotDefined()

    def showMessage(self, message):
        """
        Shows a message to the user
        """
        util.raiseNotDefined()

    def finish(self):
        """
        Terminates the display.
        """
        util.raiseNotDefined()


class ConsoleDisplay(Display):
    """
    ..
    """

    def __init__(self, gameStateData):
        Display.__init__(self, gameStateData)

    def start(self):
        """
        Starts the display.
        """
        self._refresh()

    def update(self, new_gameStateData):
        """
        Update the display with the new data supplied.
        """
        self.data = new_gameStateData
        self._refresh()

    def finish(self):
        """
        Terminates the display.
        """
        pass

    def wait(self, ms=None):
        """
        Wait for a user event.
        """
        raw_input("\n\nPress a key...")

    def showMessage(self, message):
        """
        Shows a message to the user
        """
        print message

    def askForAction(self, role, index, currPos, possActions):
        """
        Ask the user to perform an action.
        """
        print str(role) + " -> " + str(index)
        print "Current position : " + str(currPos)
        print "Possible actions : " + str(possActions)
        # request = raw_input("Destination, TicketType = ").split(',')
        request = raw_input("Destination, TicketType = ")
        while "," not in request:
            print "You missed the comma!"
            request = raw_input("Destination, TicketType = ")
        fields = request.split(",")
        dest, ticket = int(fields[0]), fields[1].strip().upper()
        return dest, ticket

    def _refresh(self):
        import os
        clear = lambda: os.system('cls')
        clear()
        print "\n\n" + "=" * 40 + "\n"
        print self.data
        print "" + "=" * 40 + "\n"



class GUIDisplay(Display):
    """
    ...
    """

    def __init__(self, gameStateData):
        Display.__init__(self, gameStateData)
        # screen
        self.screen = pygame.display.set_mode(gu.SCREEN_SIZE)
        pygame.display.set_caption("Scotland Yard")
        # game board
        self.board = pygame.Surface(gu.BOARD_SIZE)
        self.board = self.board.convert()
        self.board.fill(gu.BG_COLOR)
        # info panel
        self.infoPanel = pygame.Surface(gu.INFO_PANEL_SIZE)
        self.infoPanel = self.infoPanel.convert()
        self.infoPanel.fill(gu.INFO_PANEL_COLOR)
        # settings panel
        self.settingsPanel = pygame.Surface(gu.SETTINGS_PANEL_SIZE)
        self.settingsPanel = self.settingsPanel.convert()
        self.settingsPanel.fill(gu.SETTINGS_PANEL_COLOR)
        # moves panel
        self.movesPanel = pygame.Surface(gu.MOVES_PANEL_SIZE)
        self.movesPanel = self.movesPanel.convert()
        self.movesPanel.fill(gu.MOVES_PANEL_COLOR)
        

    def start(self):
        """
        Starts the display.
        """
        self._drawGameBoardAndInfo()
        self.STATIC_BOARD = self.board.copy() # create a copy for later
        self._drawPlayers()
        self.screen.blit(self.board, gu.BOARD_RECT)
        pygame.display.update()
        self.wait(1000)

    def update(self, new_gameStateData):
        """
        Update the display with the new data supplied.
        """
        self.data = new_gameStateData
        
        # update board
        self.board = self.STATIC_BOARD.copy()
        self._drawPlayers()
        self.screen.blit(self.board, gu.BOARD_RECT)
        # update settings panel
        self.showMessage(gu.getSettingsPanelMessage(self.data), self.settingsPanel, 
                         bg_color = gu.SETTINGS_PANEL_COLOR, 
                         rect = gu.SETTINGS_PANEL_RECT)
        # update Mr.X moves panel
        self.showMessage(gu.getMovesPanelMessage(self.data), self.movesPanel, 
                         bg_color = gu.MOVES_PANEL_COLOR, 
                         rect = gu.MOVES_PANEL_RECT)
        pygame.display.update()
        

    def wait(self, ms=None):
        """
        Wait for a user event.
        """
        if ms is None:  
            while True: # I know it doesn't make sense, but do not remove it.
                for _ in pygame.event.get():
                    pass
                return
        else:        
            pygame.time.wait(ms)


    def waitQuit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

    def showMessage(self, message, surface=None, bg_color=None, rect=None):
        """
        Shows a message to the user, the default surface is INFO PANEL.
        """
        if surface is None:
            surface = self.infoPanel        
        if bg_color is None:
            bg_color = gu.INFO_PANEL_COLOR
        if rect is None:
            rect = gu.INFO_RECT
            
        surface.fill(bg_color)  # clear from previous messages
        
        lines = message.split("\n")
        font = pygame.font.Font(None, 25)
        dy = 20
        for i, line in enumerate(lines):
            txt_surf = font.render(line, False, gu.WHITE)
            new_rect = txt_surf.get_rect().move(0, i*dy)
            surface.blit(txt_surf, new_rect)
        
        self.screen.blit(surface, rect)
        self.wait()
        pygame.display.update()

    def askForAction(self, role, index, currPos, possActions):
        """
        Ask the user to perform an action.
        """
        message = str(role) + " -> " + str(index)
        if role == AgentRole.COP or Settings.isDebug():
            message += "\nCurrent position : " + str(currPos)
            message += "\nPossible actions :\n   " + "\n   ".join([a.__repr__() for a in possActions])
        self.showMessage(message, surface=self.infoPanel, bg_color=gu.INFO_PANEL_COLOR)
        request = raw_input("Destination, TicketType = ")
        while "," not in request:
            print "You missed the comma!"
            request = raw_input("Destination, TicketType = ")
        fields = request.split(",")
        dest, ticket = int(fields[0]), fields[1].strip().upper()
        return dest, ticket

    def finish(self):
        """
        Terminates the display.
        """
        pygame.quit()

    def _drawGameBoardAndInfo(self):
        gu.drawEdges(self.board)
        gu.drawNodes(self.board)
        gu.drawNumbers(self.board)
        
        self.showMessage("Starting a new Game...", self.infoPanel, 
                         bg_color = gu.INFO_PANEL_COLOR, 
                         rect = gu.INFO_RECT)
        self.showMessage(gu.getSettingsPanelMessage(self.data), self.settingsPanel, 
                         bg_color = gu.SETTINGS_PANEL_COLOR, 
                         rect = gu.SETTINGS_PANEL_RECT)
        self.showMessage("Mr.X info", self.movesPanel, 
                         bg_color = gu.MOVES_PANEL_COLOR, 
                         rect = gu.MOVES_PANEL_RECT)

    def _drawPlayers(self):
        if Settings.isDebug() or self.data.getNumMoves() in Settings.getNotHiddenMovesNumbers():
            gu.drawAgent(self.board, self.data.getAgent(0))
        for i in range(self.data.numberOfCops()):
            gu.drawAgent(self.board, self.data.getAgent(i+1))
        
        
        
if __name__ == '__main__':
    #from agents import  MrX, KeyboardMrX, KeyboardCop, Cop
    from game import GameStateData
    from scotlandYard import createAgents
    agents_list = createAgents()
    print agents_list
    layout = Settings.getLayout()
    data = GameStateData(layout, agents_list)
    dp = GUIDisplay(data)
    dp.start()
    dp.waitQuit()
