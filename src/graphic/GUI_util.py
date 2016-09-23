'''
Created on 14/set/2016

@author: Lorenzo Selvatici
'''

from layout import EdgeType
from math import sqrt
from settings import Settings
from agents import AgentRole
import pygame
import pygame.locals

import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# initialize all modules
pygame.init()

# constants
RED = (255,0,0)
GREEN = (0,204,0)
BLUE = (51,51,205)
YELLOW = (250, 250, 0)
L_GREY = (220,220,220)
GREY = (119,136,153)
WHITE = (255,255,255)
BLACK = (0,0,0)

# COLOR SETTINGS
BG_COLOR = L_GREY
NO_STATION_COLOR = L_GREY
INFO_PANEL_COLOR = BLACK
SETTINGS_PANEL_COLOR = BLACK
MOVES_PANEL_COLOR = BLACK

# SIZE SETTINGS
N = Settings.getLayout().getNumNodes()
Ny = int(sqrt(N))
Nx = int(N/Ny if N%Ny==0 else N/Ny + 1)

BLOCK_SIZE = 70, 70

BOARD_SIZE = BLOCK_SIZE[0]*Nx,BLOCK_SIZE[1]*Ny

H = 200
INFO_PANEL_SIZE = BOARD_SIZE[0] / 2, H
SETTINGS_PANEL_SIZE = BOARD_SIZE[0] / 2, H

MOVES_PANEL_SIZE = 150, BOARD_SIZE[1] + INFO_PANEL_SIZE[1]

SCREEN_SIZE = BOARD_SIZE[0] + MOVES_PANEL_SIZE[0], MOVES_PANEL_SIZE[1]

# POSITION SETTINGS
BOARD_UPPER_LEFT = 0, INFO_PANEL_SIZE[1]
BOARD_RECT = pygame.Rect(BOARD_UPPER_LEFT, BOARD_SIZE)

INFO_UPPER_LEFT =  0, 0
INFO_RECT = pygame.Rect(INFO_UPPER_LEFT, INFO_PANEL_SIZE)  # upper left panel

SETTINGS_PANEL_UPPER_LEFT =  INFO_PANEL_SIZE[0], 0
SETTINGS_PANEL_RECT = pygame.Rect(SETTINGS_PANEL_UPPER_LEFT, SETTINGS_PANEL_SIZE)  # upper center panel

MOVES_PANEL_UPPER_LEFT = INFO_PANEL_SIZE[0] + SETTINGS_PANEL_SIZE[0], 0
MOVES_PANEL_RECT = pygame.Rect(MOVES_PANEL_UPPER_LEFT, MOVES_PANEL_SIZE)  # right panel


# EDGE SETTINGS
EDGE_WIDTH = 5
EDGE_SHIFT = {EdgeType.TAXI : (0,0),
              EdgeType.BUS : (EDGE_WIDTH, EDGE_WIDTH), # top right
              EdgeType.UNDERGROUND : (-EDGE_WIDTH, -EDGE_WIDTH), # bottom left
              EdgeType.FERRY: (-EDGE_WIDTH, -EDGE_WIDTH) # botton left, NO UNDERGROUND and FERRY at the same time!!
              }

EDGE_COLORS = {EdgeType.TAXI : YELLOW,
              EdgeType.BUS : BLUE, # top right
              EdgeType.UNDERGROUND : RED, # bottom left
              EdgeType.FERRY: GREEN # botton left, NO UNDERGROUND and FERRY at the same time!!
              }
 

NODES = Settings.getLayout().getNodesStations() # dict --> numNodes : set(EdgeType)

def hasStation(edge_type, n):
    if n not in NODES:
        return False
    return edge_type in NODES[n]

def getCenter(n):
    x, y = (n-1)%Nx, (n-1)/Nx
    topLeftCorner = x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]
    shift = BLOCK_SIZE[0] / 2, BLOCK_SIZE[1] / 2
    return topLeftCorner[0]+shift[0], topLeftCorner[1]+shift[1]

def getColor(edge_type):
    return EDGE_COLORS[edge_type]

def drawNodes(board):
    stop = False
    for j in range(Ny):
        if stop : 
            break
        for i in range(Nx):
            number = i + 1 + Nx*j
            if number>N:
                stop=True
                break
            center = getCenter(number)
            
            r=min(BLOCK_SIZE)/4
            
            # TAXI station
            color = getColor(EdgeType.TAXI) if hasStation(EdgeType.TAXI, number) else NO_STATION_COLOR
            pygame.draw.circle(board, color, center, r)
            
            # BUS station
            color = getColor(EdgeType.BUS) if hasStation(EdgeType.BUS, number) else NO_STATION_COLOR         
            pygame.draw.circle(board, color, center, r-5)
            
            # FERRY or UNDERGROUND station
            if hasStation(EdgeType.UNDERGROUND, number):
                color = getColor(EdgeType.UNDERGROUND)
            elif hasStation(EdgeType.FERRY, number):
                color = getColor(EdgeType.FERRY)
            else:
                color = NO_STATION_COLOR
            pygame.draw.circle(board, color, center, r-10)
            
    
def drawNumbers(board):
    font = pygame.font.Font(None, 20)
    stop = False
    for j in range(Ny):
        if stop : 
            break
        for i in range(Nx):
            number = i + 1 + Nx*j
            if number>N:
                stop=True
                break
            txt_surf = font.render(str(number), False, (0,0,0))
            txt_rect = txt_surf.get_rect(center = getCenter(number))
            board.blit(txt_surf, txt_rect)
            
def drawEdges(board):
    # edge format : (start, end, edgeType, path)
    for start, end, edge_type, path in Settings.getLayout().getEdges():
        point_list = [getCenter(start)] + [getCenter(i) for i in path] + [getCenter(end)]
        dx, dy = EDGE_SHIFT[edge_type]
        point_list = [(x + dx, y + dy) for x,y in point_list] 
        pygame.draw.lines(board, getColor(edge_type), False, point_list, EDGE_WIDTH)

def getSettingsPanelMessage(data):
    message = "current move : " + str(data.getNumMoves()) + "\n" + \
              "max number of moves : " + str(Settings.getMaxNumMoves()) + "\n" + \
              "not hidden moves: " + str(Settings.getNotHiddenMovesNumbers())
    if Settings.isDebug():
        message += "\n\n DEBUG MODE ON"
    
    return message

def getMovesPanelMessage(data):
    message = "  Mr.X info\n"
    not_hidden_moves = Settings.getNotHiddenMovesNumbers()
    for i in range(data.getNumMoves()):
        n_move = i + 1
        mrx_state = data.getAgentState(0)
        ticket = mrx_state.getMovesHistory()[i].getTicketType()
        message += "\n  " + str(n_move) + " : " + str(ticket)
        if n_move in not_hidden_moves:
            mrx_position = mrx_state.getPosition()
            message += "   " + str(mrx_position)
    return message
            
        
            

def load_image(name):
    import os.path
    fullname = os.path.join("C:\Users\Selvatici\Desktop\Python\Projects\ScotlandYard\Files", name)
    try:
        img = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    img = img.convert()
    return img
 

def drawAgent(board, agent):
#     if agent.getRole() == AgentRole.Mr_X:
#         img = load_image("mrx2.jpg")
#     else:
#         img = load_image("tmp1.png")
#      
#     position = agent.getAgentState().getPosition()
#     img_rect = img.get_rect(center = getCenter(position))   
#     board.blit(img, img_rect)
    color = GREEN if agent.getRole()==AgentRole.COP else RED
    center = getCenter(agent.getAgentState().getPosition())
    r = min(BLOCK_SIZE)/2
    pygame.draw.circle(board, color, center, r, 15)

if __name__ == '__main__':
    pass





