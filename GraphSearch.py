from collections import deque
from Entities import *
from States import *
import logging 
import copy
import pygame

level = logging.DEBUG	
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level =level, format=fmt)


def bfs_search(state:State,isAI,Target_treasure=None):
    
    start_state=copy.deepcopy(state)
    if Target_treasure is not None:
        for p in start_state.players:
            if not p.isAI:
                p.goal = Treasure(Target_treasure[0],Target_treasure[1],1)
        start_state = State(start_state.players,start_state.treasures,start_state.board,start_state.side_tile,start_state.forbidden_shift)
   
    # Keep track of visited nodes and the path to each node
    expandedNodes = set()

    path = {start_state: [start_state]}
    action_path = {start_state:[]}
    # Use a deque to implement the FIFO queue for the BFS algorithm
    frontier = deque()
    frontier.append(start_state)
    Initial_goal = start_state.Human_Treasure
    while frontier:

        # Choose & remove a node n from frontier
        node = frontier.popleft()
        assert node.Human_Treasure == Initial_goal
        #add n to expandedNodes
        expandedNodes.add(node)
        
        # Check if we've found the goal state
        if node.isAI_at_goal() or node.isHuman_at_goal():
            return  (path[node],path,action_path)
        
        # Add child nodes to the queue if they haven't been visited
        
        for i in range(len(node.children_move(isAI)[0])):
            child = node.children_move(isAI)[0][i]
            action= node.children_move(isAI)[1][i]
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
                action_path[child] = action_path[node] + [action]

    # If we haven't found the goal state, return None

    return (None,path,action_path)

def find_closest_to_goal(path):
    # returns a list of states that guide to the state which is closest to the AI goal
    state_list = list(path.keys())
    distances = [0]*len(state_list)
    for i in range(len(distances)):
        distances[i] = ManhattanDistance(state_list[i].AI_Pos, state_list[i].AI_Treasure)
    index_min = min(range(len(distances)), key=distances.__getitem__)
    return path[state_list[index_min]]


def bfs_search_no_goal(start_state,isAI):
    # BFS function to return all approachable states for a given player

    # Keep track of visited nodes and the path to each node
    expandedNodes = set()

    path = {start_state: [start_state]}
    
    # Use a deque to implement the FIFO queue for the BFS algorithm
    frontier = deque()
    frontier.append(start_state)
    
    while frontier:

        # Choose & remove a node n from frontier
        node = frontier.popleft()

        #add n to expandedNodes
        expandedNodes.add(node)
        
        # Add child nodes to the queue if they haven't been visited
        
        for child in node.children_move(isAI)[0]:
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
    # If we haven't found the goal state, return None
    return expandedNodes

def children_after_turn(state:State,isAI:bool):
    # Lists all the possible child states from a given state after a turn
    states_dict = {}
    children,action_list = state.children_tileshift(isAI)
    for i in range(len(children)):
        child = children[i]
        action = action_list[i]
        sol,path,action_path = bfs_search(child,isAI)
        if sol is not None:
            
            states_dict[sol[-1]] = [action] + action_path[sol[-1]]
        else: 
            for state in list(path):
                states_dict[state] = [action] + action_path[state]
    return states_dict


def ManhattanDistance(Pos1,Pos2):
    row = Pos1[0]
    col = Pos1[1]
    goal_row = Pos2[0]
    goal_col = Pos2[1]
    return abs(row-goal_row) + abs(col-goal_col)



TURN_LIMIT = 3

def minimax(state:State,turn, alpha, beta, isAI, Target_Treasure, ExpandedNodes = list(),Basic_TileShift=None):
    global TURN_LIMIT
    state.Human_Treasure = Target_Treasure
    pygame.event.pump() # Avoid freezing
    if turn >= TURN_LIMIT:

            try:                    
                eval=  1/(ManhattanDistance(state.AI_Pos,state.AI_Treasure)*turn) - 1/(ManhattanDistance(state.Human_Pos,Target_Treasure)* turn)
            except ZeroDivisionError: # In case tile out of the board 
                eval = evaluate(state)

            return Basic_TileShift,eval 

    if len(ExpandedNodes)%1000 <= 10:
        print(len(ExpandedNodes),'nodes generated')
    
    if isAI:
        maxEval = -10**99
        
        _states,_TileShifts = state.children_tileshift(isAI)
        for child,this_tileShift in zip(_states,_TileShifts):
            if child.inList(ExpandedNodes): # Only True with side_tile = Straight1 or 2
                continue
            else:
                ExpandedNodes.append(child)
            
            Solution = bfs_search(child,isAI,state.Human_Treasure)

            if Solution[0] != None:
                try:
                    return this_tileShift,1/turn
                except ZeroDivisionError:

                    return this_tileShift,1
            else:
                if None not in state.AI_Treasure: # Only moves closer to treasure if Treasure on the board, else doesn't move
                    Manhanthan_distances = dict.fromkeys(Solution[1])
                    for state in Solution[1]:
                        Manhanthan_distances[state]= ManhattanDistance(state.AI_Pos,state.AI_Treasure)

                    Manhanthan_distances = dict(sorted(Manhanthan_distances.items(), key=lambda item: item[1]))	
                    minAI = min(Manhanthan_distances.values())
                    assert minAI == list(Manhanthan_distances.values())[0]
                    child = list(Manhanthan_distances.keys())[0]
                    ExpandedNodes.append(child)

                return_value = minimax(child,turn+1, alpha, beta, False,child.Human_Treasure,ExpandedNodes,this_tileShift)
                eval = return_value[1]
                maxEval = max(maxEval, eval)
                if eval == maxEval:
                    Basic_TileShift = this_tileShift
                alpha = max(alpha, eval)
                if beta <= alpha :
                    break
        
        return Basic_TileShift,maxEval
 
    else:
        minEval = 10**99
        
        _states,_TileShifts = state.children_tileshift(isAI)
        for child,this_tileShift in zip(_states,_TileShifts):
            if child.inList(ExpandedNodes): # Only True with side_tile = Straight1 or 2
                continue            
            else:
                ExpandedNodes.append(child)

            Solution = bfs_search(child,isAI,state.Human_Treasure)

            if Solution[0] != None:
                try:
                    return this_tileShift,-1/turn
                except ZeroDivisionError:
                    return this_tileShift,-1

            else:
                if None not in state.Human_Treasure: # Only moves closer to treasure if Treasure on the board, else doesn't move
                    Manhanthan_distances = dict.fromkeys(Solution[1])
                    for state in Solution[1]:
                        Manhanthan_distances[state]= ManhattanDistance(state.Human_Pos,state.Human_Treasure)
                    
                    Manhanthan_distances = dict(sorted(Manhanthan_distances.items(), key=lambda item: item[1]))	
                    minHum = min(Manhanthan_distances.values())
                    assert minHum == list(Manhanthan_distances.values())[0]
                    child = list(Manhanthan_distances.keys())[0]
                    ExpandedNodes.append(child)

                return_value = minimax(child,turn+1, alpha, beta,True,child.Human_Treasure,ExpandedNodes,this_tileShift)
                eval = return_value[1]
                if eval == None:continue #already explored node or not evaluable
                minEval = min(minEval, eval)
                if eval == minEval:
                    Basic_TileShift = this_tileShift
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        
        return Basic_TileShift,minEval
 
 
def evaluate(state:State):
    if state.AI_Treasure[0] is None: score_AI = 0
    else: score_AI = 1/(1+ManhattanDistance(state.AI_Pos,state.AI_Treasure))
    if state.Human_Treasure[0] is None: score_Human = -1
    else: score_Human = 1/(1+ManhattanDistance(state.Human_Pos,state.Human_Treasure))
    return score_AI - score_Human
