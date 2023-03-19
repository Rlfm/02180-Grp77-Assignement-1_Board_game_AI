
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

	def actions_to_states(state:State,actions_list):
		states = []
		new_state=copy.deepcopy(state)
		for a in actions_list:
			new_state = results(new_state,a)
			states.append(new_state)
		return states
	
	def run_game():
		import Interface as game
		game.init_game(7,7)
		playing = True
		while playing:

			CurrentTiles = random_board(7)
			Treasure_P1 = Treasure(6,6,0) 
			Treasure_P2 = Treasure(6,0,1)
			AI = Player(0,6,Treasure_P2,True)
			Human = Player(0,0,Treasure_P1,False)
			side_tile = copy.deepcopy(CurrentTiles[random.randint(0,6)][random.randint(0,6)])
			start_state= State([AI,Human],[Treasure_P1,Treasure_P2],CurrentTiles,side_tile,None)

			game.display_state(start_state)
			current_state = start_state

			while not(current_state.isAI_at_goal() or current_state.isHuman_at_goal()):
				if not current_state.isAI_at_goal():
					current_state = game.human_turn(current_state)
				time.sleep(2)
				if not current_state.isHuman_at_goal():
					state_seq = AI_turn(current_state)
					game.AUDIO_DICT['AIready'].play()
					game.pygame.event.pump()
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
			
	def random_board(size):
		board =[[None for i in range(size)] for i in range(size)]
		empty_tiles = size**2
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
		empty_tiles-= 4 + 4*len(evens)
		
		StraightTiles = [random.choice([Straight1,Straight2]) for _ in range(round(empty_tiles*0.5))]
		CornerTiles = [random.choice([Corner1,Corner2,Corner3,Corner4]) for _ in range(round(empty_tiles*0.3))]
		T_Tiles = [random.choice([T_1,T_2,T_3,T_4]) for _ in range(round(empty_tiles*0.2))]

		TilesProportion = StraightTiles + CornerTiles +  T_Tiles
		for n in range(empty_tiles - len(TilesProportion)):
			TilesProportion.append(random.choice(Tiles))
	
		for i in range(size):
			for j in range(size):
				if board[i][j] is None:
					tile = random.choice(TilesProportion)
					board[i][j] = tile
					TilesProportion.remove(tile)

		return board


	run_game()



if __name__ == '__main__':
	main()