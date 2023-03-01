

def progress_bar(progress,total):

	percent = 100 * (progress/float(total))
	bar = "█" * int(percent) + "░" *(100-int(percent))
	print(f"\r{bar} {percent:.2f}%",end="\r")
	if percent >= 100:
		print("\r" + 110*" ",end="\r")

from LabyrinthClasses import State, MoveAction, Tile,actions,results,TileShiftAction
from GraphSearch import bfs_search
import random
import os 
from termcolor import colored
import copy
import time

os.system("clear") 

"""
Corner1 =  [[" "," "," "],
			[" ","█","█"],
			[" ","█"," "],
	   ]

Corner2 =  [[" ","█"," "],
			[" ","█","█"],
			[" "," "," "],
	   ]

Corner3 =  [[" ","█"," "],
			["█","█"," "],
			[" "," "," "],
	   ]

Corner4 =  [[" "," "," "],
			["█","█"," "],
			[" ","█"," "],
	   ]


T_1 =  [    [" ","█"," "],
			[" ","█","█"],
			[" ","█"," "],
	   ]

T_2 =  [    [" ","█"," "],
			["█","█","█"],
			[" "," "," "],
	   ]

T_3 =  [    [" ","█"," "],
			["█","█"," "],
			[" ","█"," "],
	   ]

T_4 =  [    [" "," "," "],
			["█","█","█"],
			[" ","█"," "],
	   ]


Straight1 =  [  [" ","█"," "],
				[" ","█"," "],
				[" ","█"," "],
	   ]


Straight2 =  [  [" "," "," "],
				["█","█","█"],
				[" "," "," "],
	   ]

"""

Corner1 = Tile(0,1,1,0)
Corner2 = Tile(1,1,0,0)
Corner3 = Tile(1,0,0,1)
Corner4 = Tile(0,0,1,1)
T_1 = Tile(1,1,1,0)
T_2 = Tile(1,1,0,1)
T_3 = Tile(1,0,1,1)
T_4 = Tile(0,1,1,1)
Straight1 = Tile(1,0,1,0)
Straight2 = Tile(0,1,0,1)

Tiles = [Corner1,Corner2,Corner3,Corner4,T_1,T_2,T_3,T_4,Straight1,Straight2]


NB_COL_ROW = 5
assert NB_COL_ROW%2 !=0
	


#-------------------------- Board generation ---------------------
#Tiles = {0:Corner1,1:Corner2,2:Corner3,3:Corner4,4:T_1,5:T_2,6:T_3,7:T_4,8:Straight1,9:Straight2}
Board = [[] for _ in range(NB_COL_ROW)]
CurrentTiles = [[] for _ in range(NB_COL_ROW)]
for n in range(5):
	for _ in range(5):
		new_tile = copy.deepcopy(random.choice(Tiles))
		CurrentTiles[n].append(new_tile)
		Board[n].append(new_tile.ASCII)

Treasures_positions = [(0,2),(0,4),(2,0),(2,2),(2,4),(4,2),(4,4),(4,0)]

Treasure_P1 = random.choice(Treasures_positions)
Treasures_positions.remove(Treasure_P1)
Treasure_P2 = random.choice(Treasures_positions)

Player_1 = [4,4] #Changed to array (not tuple) in order to be modified
Player_2 = [0,0]


CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles,[copy.deepcopy(Straight1),copy.deepcopy(Straight1)])

#-------------------------- Board Display -------------------

def Display():
	global Board
	screen_rows = list()

	Board[Treasure_P1[0]][Treasure_P1[1]][1][1] = colored("$","blue")
	Board[Treasure_P2[0]][Treasure_P2[1]][1][1] = colored("£","red")
	
	Board[Player_1[0]][Player_1[1]][1][1] = colored("█","blue")
	Board[Player_2[0]][Player_2[1]][1][1] = colored("█","red")

	board_display = list()
	for row_nb in range(NB_COL_ROW):
		for char_row in range(3):
			row = f"         ░{'░'.join([''.join(Board[row_nb][col][char_row]) for col in range(NB_COL_ROW)])}░"
			board_display.append(row)
		
		if row_nb != NB_COL_ROW-1:
			board_display.append(f"         {(len(row)-9)*'░'}")

	screen_rows = ["","","","","",f"         {(len(row)-9)*'░'}"] + board_display + [f"         {(len(row)-9)*'░'}","","","","",""]

	for row in screen_rows:
		print(row)

Display()

##BFS TESTING

CurrentTiles = [[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Corner2),copy.deepcopy(Corner4),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight2),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],]


Player_1 = [4,4]
Player_2 = [0,0]
Treasure_P1 = [3,2] # /!\ Treasures shouldn't be on moving tiles /!\ Only good for testing 
Treasure_P2 = [4,0]

side_tile =Tile(1,1,1,1) #This type of tile shouldn't exist; just for testing purposes
CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles,[side_tile])

CurrentState.display()

Solution = bfs_search(CurrentState)

def animate_states(states):
    for state in states:
        print("\033c", end="")
        state.display()
        time.sleep(1)
	
if Solution[0] is not None:
	print("SOLUTION FOUND WITH THE FOLLOWING STEPS:")
	animate_states(Solution[0])
else: 
	print("NO SOLUTION FOUND")
	animate_states(Solution[1])


#TILE SHIFT TESTING
print('3RD ROW TILE SHIFT IN DIRECTION +1')
shift = TileShiftAction([side_tile],True,3,-1)
results(CurrentState,shift).display()