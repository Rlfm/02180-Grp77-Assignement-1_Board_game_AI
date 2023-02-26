

def progress_bar(progress,total):

	percent = 100 * (progress/float(total))
	bar = "█" * int(percent) + "░" *(100-int(percent))
	print(f"\r{bar} {percent:.2f}%",end="\r")
	if percent >= 100:
		print("\r" + 110*" ",end="\r")

from LabyrinthClasses import State, Action, Tile,actions
from GraphSearch import bfs_search
import random
import os 
from termcolor import colored
import copy

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

Corner1 = Tile("C1",0,1,1,0)
Corner2 = Tile("C2",1,1,0,0)
Corner3 = Tile("C3",1,0,0,1)
Corner4 = Tile("C4",0,0,1,1)
T_1 = Tile("T1",1,1,1,0)
T_2 = Tile("T2",1,1,0,1)
T_3 = Tile("T3",1,0,1,1)
T_4 = Tile("T4",0,1,1,1)
Straight1 = Tile("S1",1,0,1,0)
Straight2 = Tile("S2",0,1,0,1)

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


CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles)

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
Treasure_P1 = [3,2]
Treasure_P2 = [4,0]

CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles)

CurrentState.display()
for s in CurrentState.childs():
	s.display()
	print(s.AI_Pos)
	print(s.board[0][0].ASCII)
	for a in actions(s):
		print(a)
	for ss in s.childs():
		ss.display()
		print(ss.AI_Pos)
Solution = bfs_search(CurrentState)

if Solution is not None:
	print("SOLUTION FOUND WITH THE FOLLOWING STEPS:")
	for t in Solution:
		t.display()
else: print("NO SOLUTION FOUND")