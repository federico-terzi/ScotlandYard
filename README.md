# ScotlandYard
Scotland Yard, a popular strategic game.

Scotland Yard is a popular stategic game, really straightforward and easy to learn, but still very amusing to play with. However my interest goes beyond playing with it: on my part it's a perfect platform to start coding some AI and ML algorithms.

A nice GUI (still needing of some improvements) allows you to see and appreciates what your algorithm is doing under the surface. You can test and experiment as you wish.

Before running the main file (scotlandYard.py) there are still few things you have to take care about.
- make sure you have installed both Python 2.7 (https://www.python.org/downloads/) and Pygame (http://www.pygame.org/download.shtml).
- edit the settings.txt file (change the LAYOUT_FILENAME path to be consistent with your working directory)
- edit the SETTINGS_FILE_NAME at line 9 in settings.py

If you want to switch to your own agent change the MrX_TYPE or COPS_TYPE in settings.txt
example: if you have created an agent called "SuperAgentMrX" you should put: MrX_TYPE -> SuperAgent (pay attention to CAPITAL letters). 

** RULES of SCOTLAND YARD **
Mr.X is escaping from the COPS. His objective is to not get caught before the end of the game. 
The board game can be seen as an undirected graph, where the nodes are the stations and the edges are the links between them. Stations and links are of different types (colors): taxi, bus, underground, ferry. 
A player can use a specific transport if and only if:
- he has a ticket for it
- he is on a node which has the station for that kind of transport

The first player to move is Mr.X. His position is hidden for most of the time, he only shows up on particular moves (see NOT_HIDDEN_MOVES in settings.txt). Therefore, his objective is to be in a position as safe as possible when it comes the time to show himself. During the other moves, the cops know only the type of the ticket that Mr.X have used so they are constantly sharpening their beliefs.

Next it's Cops' turn, they move one at a time in a specific order and they aim to end up in the same position of Mr.X so that they catch him. The cops should cooperate in order to achieve this goal and be as smart as possible in guessing Mr.X position.

The game goes on until one of the two sides wins.
Mr.X wins if:
  - the max number of moves is reached.
  - the cops cannot move (no legal moves are possible with the ticket they own)
Cops win if:
  - a cop is in the same position of Mr.X at the same time.
  - Mr.X is surrounded and cannot move.

The version explained on wikipedia is slightly different (https://en.wikipedia.org/wiki/Scotland_Yard_(board_game)), but it gives the idea.

Now it's time to code and have fun! Create your own Mr.X and Cop agents. 

Feel free to contact me and fix bugs,
Lorenzo
