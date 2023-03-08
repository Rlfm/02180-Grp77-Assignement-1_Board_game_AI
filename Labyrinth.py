
from States import *
from GraphSearch import *
import random
import os 
from termcolor import colored
import copy
import time

import logging  
level = logging.DEBUG	
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level =level, format=fmt)

os.system("clear") 


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


##BFS TESTING

CurrentTiles = [[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Corner4),copy.deepcopy(Corner4),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight1),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],]


def random_board():
	StraightTiles = [random.choice([Straight1,Straight2]) for _ in range(round(NB_COL_ROW**2*0.5))]
	CornerTiles = [random.choice([Corner1,Corner2,Corner3,Corner4]) for _ in range(round((NB_COL_ROW**2)*0.3))]
	T_Tiles = [random.choice([T_1,T_2,T_3,T_4]) for _ in range(round((NB_COL_ROW**2)*0.2))]

	TilesProportion = StraightTiles + CornerTiles +  T_Tiles
	for n in range(NB_COL_ROW**2 - len(TilesProportion)):
		TilesProportion.append(random.choice(Tiles))
 
	board = list()
	for _ in range(NB_COL_ROW):
		row = list()
		for n in range(NB_COL_ROW):
			tile = random.choice(TilesProportion)
			row.append(copy.deepcopy(tile))
			TilesProportion.remove(tile)
		board.append(row)

	return board

#CurrentTiles = random_board()

Treasure_P1 = Treasure(1,3,0) 
Treasure_P2 = Treasure(4,0,1)
AI = Player(0,0,Treasure_P2,True)
Human = Player(3,4,Treasure_P1,False)

side_tile =Tile(1,1,0,1) #This type of tile shouldn't exist; just for testing purposes
#CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles,side_tile)
CurrentState = State([AI,Human],[Treasure_P1,Treasure_P2],CurrentTiles,side_tile,TileShiftAction(None,False,3,1))
CurrentState.display()

Solution = bfs_search(CurrentState,True)

def animate_states(states):
    for state in states:
        print("\033c", end="")
        state.display()
        time.sleep(0.2)
	
if Solution[0] is not None:
	print("SOLUTION FOUND WITH THE FOLLOWING STEPS:")
	animate_states(Solution[0])
else: 
	print("NO SOLUTION FOUND")
	animate_states(Solution[1])

"""
Applicable_TileShifs= list(dict.fromkeys(actions(CurrentState,TileShiftAction,isAI=True))) #Avoid repetition with Straight only 2 rotation VS 4 for others
TileShifts_groups = dict.fromkeys([TS.new_tile for TS in Applicable_TileShifs],[])
"""

start = time.perf_counter()
Minimax_return = dict()
for TileShiftX in actions(CurrentState,TileShiftAction,isAI=True):
	state = results(CurrentState,TileShiftX)
	Minimax_return[TileShiftX] = minimax(state,turn=0,alpha=-10**99,beta=10**99,isAI=True,Target_Treasure=CurrentState.Human_Treasure)

for TileShiftX,value in Minimax_return.items():
	print(f"{str(TileShiftX)} -> {value}")

stop = time.perf_counter()

print(f"Time elapsed {round(stop-start)}s ")
"""
#TILE SHIFT TESTING
shift = TileShiftAction(side_tile,True,3,-1)
print(shift)
results(CurrentState,shift).display()
tile_shifts = actions(CurrentState,TileShiftAction,True)
for a in tile_shifts:
	print(a)
"""


