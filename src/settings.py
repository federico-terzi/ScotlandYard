'''
Created on 09/set/2016

@author: Lorenzo Selvatici
'''
from layout import Layout
import util

"""
Uncomment the variable "SETTINGS_FILE_NAME" if you want to load another settings file,
leave it like this if you want to use the default one"
"""
#SETTINGS_FILE_NAME = "C:\Users\Selvatici\Desktop\Python\Projects\ScotlandYard\Files\settings.txt"
SETTINGS_FILE_NAME = "DEFAULT"
SETTINGS_SEPARATOR = "->"


class Settings:
    """
    The settings are stored as a dictionary, the keys represent the options' name.
    """
    
    settings = {}
    layout = None
    positions = None
    
    def _getSettingsAsDict():
        """
        Returns the settings as a dictionary.
        Possible keys:
        *- "DEBUG_MODE" , True or False
        *- "DISPLAY_TYPE" , the type of the display
        *- "MrX_TYPE" , Mr.X type of instance : Keyboard, ..
        *- "COPS_TYPE" , Cop type of instance : Keyboard, ..
        *- "LAYOUT_FILENAME", the path of the layout file name (.txt)
        *- "MAX_NUM_MOVES" , the max number of moves of Mr.X for one game
        *- "INITIAL_MrX_POSITION" , an integer or the string "random"
        *- "INITIAL_COPS_POSITION" , a list (size = "NUMBER_OF_COPS" ) of integer or the 
                                    string "random" separated by commas (the order matters)
        *- "NOT_HIDDEN_MOVES" , the numbers of not hidden moves : a list of integers separated by commas.
        *- "MrX_TICKETS" , format: <TicketType>=<int> ; <TicketType>=<int>; ... 
        *- "COPS_TICKETS" , format: <TicketType>=<int> ; <TicketType>=<int>; ...
         ...
        """
        # initialize setting dictionary
        if len(Settings.settings)==0:
            Settings._loadSettings(SETTINGS_FILE_NAME)
        
        # initialize the layout
        if Settings.layout is None:
            Settings.layout = Layout(Settings.settings["LAYOUT_FILENAME"])
        
        #if Settings.positions is None:
        #    Settings._assignPositions()
            
        return Settings.settings
    _getSettingsAsDict=staticmethod(_getSettingsAsDict)
    
    def _loadSettings(fileName):
        """
        Loads from the specified text file the setting of the game as a Dictionary.
        The file has to be in the format:
        <key> SETTINGS_SEPARATOR <val>
        """
        import os
        assert type(fileName) == type("string")
        
        if fileName=="DEFAULT": #Load the default settings
            baseDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fileName = baseDirectory + os.sep + "Files" + os.sep + "settings.txt"

        if not fileName.endswith(".txt"):
            fileName = fileName + ".txt"
        if not os.path.exists(fileName):
            raise ValueError(fileName + " does not exist.")
        in_file = open(fileName, "r")
        for line in in_file.readlines():
            key, val = line.strip().split(SETTINGS_SEPARATOR)
            Settings.settings[key.strip()]=val.strip()
        in_file.close()
    _loadSettings=staticmethod(_loadSettings)
    
    ########################################
    #    ACCESSOR METHODS FOR SETTINGS     #
    ########################################
    
    def isDebug():
        """
        Returns True if debug mode is on, False otherwise.
        """
        return Settings._getSettingsAsDict()["DEBUG_MODE"].upper()=="TRUE"
    isDebug = staticmethod(isDebug)
    
    def getLayout():
        """
        Returns the layout (Layout in layout.py).
        """
        if Settings.layout is None:
            Settings.layout = Layout(Settings._getSettingsAsDict()["LAYOUT_FILENAME"])
        return Settings.layout
    getLayout = staticmethod(getLayout)
    
    def getDisplayType():
        """
        Returns the display type (see display.py).
        Possibilities:
        - Console
        - GUI
        
        """
        return Settings._getSettingsAsDict()["DISPLAY_TYPE"]
    getDisplayType = staticmethod(getDisplayType)
    
    def getMrXType():
        """
        Returns the type of instance for Mr.X.
        Possibilities:
        - Keyboard
        - ...
        
        """
        return Settings._getSettingsAsDict()["MrX_TYPE"]
    getMrXType = staticmethod(getMrXType)
    
    def getCopsType():
        """
        Returns the type of instance for the Cops.
        Possibilities:
        - Keyboard
        - Smart
        
        """
        return Settings._getSettingsAsDict()["COPS_TYPE"]
    getCopsType = staticmethod(getCopsType)
    
    def getMaxNumMoves():
        """
        Returns the maximum number of moves which can be done in single game.
        """
        return int(Settings._getSettingsAsDict()["MAX_NUM_MOVES"])
    getMaxNumMoves=staticmethod(getMaxNumMoves)
    
    def getNumberOfCops():
        """
        Returns the number of Cops
        """
        if Settings.positions is None:
            Settings._assignPositions()
        return len(Settings.positions) - 1
    getNumberOfCops = staticmethod(getNumberOfCops)
    
    def getInitialMrXTickets():
        """
        Returns the initial amount of tickets for Mr.X as a Dictionary.
        """
        val = Settings._getSettingsAsDict()["MrX_TICKETS"]
        return Settings._parseTicketDict(val)
    getInitialMrXTickets = staticmethod(getInitialMrXTickets)
    
    def getInitialCopsTickets():
        """
        Returns the initial amount of tickets for the Cops as a Dictionary.
        """
        val = Settings._getSettingsAsDict()["COPS_TICKETS"]
        return Settings._parseTicketDict(val)
    getInitialCopsTickets = staticmethod(getInitialCopsTickets)
        
    def getInitialMrXPosition():
        """
        Returns the initial Mr.X position.
        """
        if Settings.positions is None:
            Settings._assignPositions()
        return Settings.positions[0]
    getInitialMrXPosition = staticmethod(getInitialMrXPosition)
    
    def getInitialCopsPositions(index=None):
        """
        Returns the position of the cop with the specified index (an integer in the interval [1, numberOfCops]
        """
        if Settings.positions is None:
            Settings._assignPositions()
        if index is not None:
            return Settings.positions[index]
        else:
            return [Settings.getInitialCopsPositions(i+1) for i in range(Settings.getNumberOfCops())]
    getInitialCopsPositions = staticmethod(getInitialCopsPositions)
    
    def getLegalPositions():
        """
        Returns the list of the legal positions.
        """
        positions = Settings.getLayout().getNodesStations().keys()
        cops = Settings.getInitialCopsPositions()
        return [pos for pos in positions if pos not in cops]
    getLegalPositions = staticmethod(getLegalPositions)
        
    def getNotHiddenMovesNumbers():
        """
        Returns the list of moves in which Mr.x will show his own positions.
        """
        return [int(x) for x in Settings._getSettingsAsDict()["NOT_HIDDEN_MOVES"].split(",")]
    getNotHiddenMovesNumbers = staticmethod(getNotHiddenMovesNumbers)
    
    #####################################################
    #    HELPER METHODS (do not call them directly)     #
    #####################################################
    
    _occupied_positions = [] # avoid that two random initial positions overlap
    
    def _assignPositions():
        mrx = Settings._getSettingsAsDict()["INITIAL_MrX_POSITION"]
        cops  = Settings._getSettingsAsDict()["INITIAL_COPS_POSITION"].split(',')
        
        legal_pos = Settings.layout.getNodesStations()  # dict --> numNodes : stationsType..
        # node number must be a key in legal pos dict
        Settings.positions = [mrx] + cops
        for i, p in enumerate(Settings.positions):
            if p.strip() != "random":
                Settings.positions[i] = int(p)
                # check it is a legal position
                assert int(p) in legal_pos, "No station for node " + p
            else:
                Settings.positions[i] = p.strip()
        
        # first assign fixed positions
        Settings._occupied_positions = [x for x in Settings.positions if type(x) == int]
        # assert there are no duplicates
        assert len(set(Settings._occupied_positions))==len(Settings._occupied_positions)
        
        # then deal with random positions
        for i, p in enumerate(Settings.positions):
            if p == "random":
                Settings.positions[i] = Settings._randomNode()
        
    _assignPositions = staticmethod(_assignPositions)
       
    def _randomNode():
        """
        This is a private function, to generate a random nodes during the game use Rules.getRandomNode()
        """
        legal_pos = Settings.layout.getNodesStations().keys()  # list of legal positions
        import random
        pos = random.choice(legal_pos)
        while pos in Settings._occupied_positions:
            pos = random.choice(legal_pos)
        Settings._occupied_positions.append(pos) # updates the occupied positions
        return pos
    _randomNode = staticmethod(_randomNode)
    
    def _parseTicketDict(sDict):
        result = {}
        for pair in sDict.strip().split(";"):
            key, val = pair.split("=")
            result[key.strip()]=int(val)
        return result
    _parseTicketDict=staticmethod(_parseTicketDict)

if __name__ == '__main__':
    print Settings.getNotHiddenMovesNumbers()
#     for key, val in Settings._getSettingsAsDict().items():
#         print "%s : %s" % (key, val)





