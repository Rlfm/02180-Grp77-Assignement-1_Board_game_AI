
from States import *
from GraphSearch import *
import random
import os 
from termcolor import colored
import copy
import time
from multiprocessing import Pool
import logging  
level = logging.DEBUG	
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level =level, format=fmt)

def main():
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

	def AI_random_turn(state:State):
		# Returns a random admissible state sequence for the AI
		state_seq = []
		tile_shift = None
		odds = [num for num in range(state.size[0]) if num % 2 != 0]
		while tile_shift == None:
			ts = TileShiftAction(state.side_tile,random.randint(0,1),odds[random.randint(0,len(odds)-1)],random.randint(0,1))
			if not ts.is_forbidden(state):
				tile_shift = ts

		resulting_state = results(state,tile_shift)
		state_seq.append(resulting_state)
		bfs = bfs_search(resulting_state,True)
		if bfs[0] is not None:
			print('AI WON')
			state_seq += bfs[0]
		else:
			approachable_states = list(bfs[1])
			random_state = approachable_states[random.randint(0,len(approachable_states)-1)]
			state_seq = state_seq + bfs[1][random_state]
		print(state_seq)
		return state_seq
	
	def AI_turn(state):
		# Returns a list of states corresponding to what the AI would do with the given state
		print('Initiated decision algorithm')

		# Select the right tile shift action
		start_time = time.perf_counter()
		TileShiftX,value = minimax(state,1,-10**99,10**99,True,state.Human_Treasure)

		print(f"Current state minimax = {value}, {TileShiftX}")
		print(f"Time elapsed {round(time.perf_counter()-start_time)}s ")

		result_state = results(state,TileShiftX)

		# Select the right pawn movement
		
		# try to find a solution
		sol,path,_ = bfs_search(result_state,True,result_state.Human_Treasure)
		
		# if no solution, just move the pawn closer to the goal
		if sol == None:
			sol = find_closest_to_goal(path)

		return sol

	def run_game(start_state):
		import Interface as game
		game.init_game(7,7)
		playing = True
		while playing:

			CurrentTiles = random_board(7)
			Treasure_P1 = Treasure(6,6,0) 
			Treasure_P2 = Treasure(6,0,1)
			AI = Player(0,6,Treasure_P2,True)
			Human = Player(0,0,Treasure_P1,False)
			start_state= State([AI,Human],[Treasure_P1,Treasure_P2],CurrentTiles,side_tile,TileShiftAction(None,False,3,1))

			game.display_state(start_state)
			current_state = start_state

			while not(current_state.isAI_at_goal() or current_state.isHuman_at_goal()):
				if not current_state.isAI_at_goal():
					current_state = game.human_turn(current_state)
				time.sleep(2)
				if not current_state.isHuman_at_goal():
					'''
					timer = time.perf_counter()
					print('Initiated Minimax')
					best_value,best_moves=alpha_beta_pruning_test(current_state,depth=1, alpha=float('-inf'), beta=float('inf'), expandedNodes=[])
					print('search time =', time.perf_counter()-timer)
					
					print('best_value= ',best_value)
					print('actions:')
					for a in best_moves:
						print(a)
					'''
					state_seq = AI_turn(current_state)
					game.AUDIO_DICT['AIready'].play()
					time.sleep(1)

					#state_seq = AI_random_turn(current_state)
					game.display_state_sequence(state_seq)
					current_state =state_seq[-1]
			if current_state.isHuman_at_goal():
				print('HUMAN WON')
				game.AUDIO_DICT['HumanWon'].play()
			else:
				print('AI WON')
				game.AUDIO_DICT['HumanLost'].play()
			game.game_ended()
			

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

	CurrentTiles = [[copy.deepcopy(Straight2),copy.deepcopy(Straight1),copy.deepcopy(Straight2),copy.deepcopy(Straight1),copy.deepcopy(Straight2)],
			[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight2),copy.deepcopy(Straight1)],
			[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
			[copy.deepcopy(Corner4),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
			[copy.deepcopy(Straight2),copy.deepcopy(Straight1),copy.deepcopy(Straight2),copy.deepcopy(Straight1),copy.deepcopy(Straight2)],]



	def random_board(size):

		StraightTiles = [random.choice([Straight1,Straight2]) for _ in range(round(size**2*0.5))]
		CornerTiles = [random.choice([Corner1,Corner2,Corner3,Corner4]) for _ in range(round((size**2)*0.3))]
		T_Tiles = [random.choice([T_1,T_2,T_3,T_4]) for _ in range(round((size**2)*0.2))]

		TilesProportion = StraightTiles + CornerTiles +  T_Tiles
		for n in range(size**2 - len(TilesProportion)):
			TilesProportion.append(random.choice(Tiles))
	
		board = list()
		for _ in range(size):
			row = list()
			for n in range(size):
				tile = random.choice(TilesProportion)
				row.append(copy.deepcopy(tile))
				TilesProportion.remove(tile)
			board.append(row)

		board[0][0] = copy.deepcopy(Corner1)
		board[-1][0] = copy.deepcopy(Corner2)
		board[-1][-1]= copy.deepcopy(Corner3)
		board[0][-1] = copy.deepcopy(Corner4)
		evens = [num for num in range(size) if num % 2 == 0 and num>0 and num<size-1]
		for e in evens:
			board[e][0] = copy.deepcopy(T_1)
			board[-1][e] = copy.deepcopy(T_2)
			board[e][-1] = copy.deepcopy(T_3)
			board[0][e] = copy.deepcopy(T_4)

		return board

	#CurrentTiles = random_board()

	Treasure_P1 = Treasure(1,3,0) 
	Treasure_P2 = Treasure(4,0,1)

	AI = Player(0,0,Treasure_P2,True)
	Human = Player(3,4,Treasure_P1,False)

	side_tile =Tile(1,1,0,0) 
	#CurrentState = State(Player_1,Player_2,Treasure_P1,Treasure_P2,CurrentTiles,side_tile)
	CurrentState = State([AI,Human],[Treasure_P1,Treasure_P2],CurrentTiles,side_tile,TileShiftAction(None,False,3,1))
	CurrentState.display()

	run_game(CurrentState)
	"""
	Solution = bfs_search(CurrentState,True)
	children = children_after_turn(CurrentState,True)
	print(len(children))

	if True:
		alpha_beta = alpha_beta_pruning_test(CurrentState,2,float('-inf'),float('inf'))
		print(alpha_beta[0])
		for a in alpha_beta[1]:
			print(a)
	"""
	def animate_states(states):
		for state in states:
			print("\033c", end="")
			state.display()
			time.sleep(0.3)
		
	"""
	if Solution[0] is not None:
		print("SOLUTION FOUND WITH THE FOLLOWING STEPS:")
		#animate_states(Solution[0])

	else: 
		print("NO SOLUTION FOUND")
		#animate_states(list(Solution[1]))

	Applicable_TileShifs= list(dict.fromkeys(actions(CurrentState,TileShiftAction,isAI=True))) #Avoid repetition with Straight only 2 rotation VS 4 for others
	TileShifts_groups = dict.fromkeys([TS.new_tile for TS in Applicable_TileShifs],[])
	"""

	"""
	start1 = time.perf_counter()
	Minimax_return = dict()

	plus1_states = list()
	for TileShiftX in actions(CurrentState,TileShiftAction,isAI=True):
		Minimax_return[TileShiftX] = "???"
		plus1_states.append((results(CurrentState,TileShiftX),1,-10**99,10**99,True,CurrentState.Human_Treasure))
	with Pool() as pool:
		Pool_results = pool.starmap(minimax,plus1_states)

	for i,value in enumerate(Pool_results):
		key = list(Minimax_return.keys())[i]
		Minimax_return[key] = value
	for TileShiftX,value in Minimax_return.items():
		print(f"{str(TileShiftX)} -> {value}")
	"""
	start1 = time.perf_counter()

	TileShiftX,value = minimax(CurrentState,1,-10**99,10**99,True,CurrentState.Human_Treasure)
	print(f"Current state minimax = {value}, {TileShiftX}")

	stop1 = time.perf_counter()
	print(f"Time elapsed {round(stop1-start1)}s ")
	
	result_from_shift = results(CurrentState,TileShiftX)
	Solution = bfs_search(result_from_shift,True,result_from_shift.Human_Treasure)

	states_to_anim = [CurrentState,result_from_shift] + Solution[0]
	animate_states(states_to_anim)

	"""
	#TILE SHIFT TESTING
	shift = TileShiftAction(side_tile,True,3,-1)
	print(shift)
	results(CurrentState,shift).display()
	tile_shifts = actions(CurrentState,TileShiftAction,True)
	for a in tile_shifts:
		print(a)
	"""


if __name__ == '__main__':
	main()