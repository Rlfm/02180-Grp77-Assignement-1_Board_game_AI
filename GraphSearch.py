from collections import deque
from Entities import *
from States import *
import logging 
import copy

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
    
    while frontier:

        # Choose & remove a node n from frontier
        node = frontier.popleft()

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


def A_star(start_state:State):

    start_state.size
    """
    row_shifts = [TileShiftAction(start_state.side_tile,True,n,1) for n in range(start_state.size[0]) if n%2 !=0] + [TileShiftAction(start_state.side_tile,True,n,-1) for n in range(start_state.size[0]) if n%2 !=0]
    col_shifts = [TileShiftAction(start_state.side_tile,False,n,1) for n in range(start_state.size[0]) if n%2 !=0] + [TileShiftAction(start_state.side_tile,False,n,-1) for n in range(start_state.size[0]) if n%2 !=0]

    print(f"{start_state.forbidden_shift=}")
    shifts = [x for x in row_shifts + col_shifts if x != start_state.forbidden_shift]
    """
    shifts = actions(start_state,TileShiftAction,True)
    heuristic_TileShift = {i:0 for i in range(len(shifts))}
    for i,shift in enumerate(shifts):
        Potential_state = results(start_state,shift)
        
        bfs_solution = bfs_search(Potential_state,True)
        if bfs_solution[0] != None:
            raise ValueError(f"first move at {i}")
            return shift
        else:
            Manhanthan_distances = dict.fromkeys(bfs_solution[1])
            for state in bfs_solution[1]:
                Manhanthan_distances[state]= ManhattanDistance(state.AI_Pos,state.AI_Treasure)
            
            Manhanthan_distances = dict(sorted(Manhanthan_distances.items(), key=lambda item: item[1], reverse = True))	
            minAI = min(Manhanthan_distances.values())

        if bfs_solution[0] != None:
            del heuristic_TileShift[i]
            continue   

        else: # Calculate Manhatan distance for P1 to all Treasures 
            Manhanthan_distances = list()
            for potential_treasure in [x for x in start_state.treasures if x != start_state.AI_Treasure]:
                pos = (potential_treasure.row, potential_treasure.col)
                for state in list(bfs_search(Potential_state,False)[1]):
                    Manhanthan_distances.append(ManhattanDistance(state.Human_Pos,pos))
            
            minP1 = min(Manhanthan_distances)
        
        h = minAI-minP1
        heuristic_TileShift[i] = h

    sorted_by_H = dict(sorted(heuristic_TileShift.items(), key=lambda item: item[1], reverse = True))	
    print(f"{sorted_by_H=}")
    for i,elet in enumerate(shifts):
        print(f"{i=} {elet} {elet.isRowShift=}")

    return shifts[list(sorted_by_H.keys())[0]]





"""
#TILE SHIFT TESTING
shift = TileShiftAction(side_tile,True,3,-1)
print(shift)
results(CurrentState,shift).display()
tile_shifts = actions(CurrentState,TileShiftAction)
for a in tile_shifts:
	print(a)
"""

TURN_LIMIT = 5
def minimax(state:State,turn, alpha, beta, isAI, Target_Treasure, ExpandedNodes = list()):
    
    state.Human_Treasure = Target_Treasure
    print(f"{state.Human_Treasure=} VS {Target_Treasure}")

    Solution = bfs_search(state,isAI,state.Human_Treasure)

    if Solution[0] != None:
        try:
            if isAI:
                print(f"SOLUTION FOR IA FOUND -> {turn}, H={1/turn}")
                return 1/turn
            else:
                print(f"SOLUTION FOR HUMAN FOUND -> {turn}, H={-1/turn}")
                return -1/turn
        except ZeroDivisionError:
            if isAI:
                print(f"SOLUTION FOR IA FOUND -> {turn}, H={1}")
                return 1
            else:
                print(f"SOLUTION FOR HUMAN FOUND -> {turn}, H={-1}")
                return -1
    
    elif turn >= TURN_LIMIT:

            try:                    
                eval=  1/(ManhattanDistance(state.AI_Pos,state.AI_Treasure)*turn) +  1/(ManhattanDistance(state.Human_Pos,Target_Treasure)* turn)
            except ZeroDivisionError: # In case tile out of the board 
                eval = None

            print(f"{state.Human_Pos=} VS {state.Human_Treasure=}, {state.AI_Pos=} VS {state.AI_Treasure=} -> {eval=}")
            return eval 

    
    else:
        if isAI and None not in state.AI_Treasure:
            Manhanthan_distances = dict.fromkeys(Solution[1])
            for state in Solution[1]:
                Manhanthan_distances[state]= ManhattanDistance(state.AI_Pos,state.AI_Treasure)

            Manhanthan_distances = dict(sorted(Manhanthan_distances.items(), key=lambda item: item[1]))	
            minAI = min(Manhanthan_distances.values())
            state = list(Manhanthan_distances.keys())[0]
            ExpandedNodes.append(state)
            #print(f"{hash(state)} -> {minAI=}")
        
        elif None not in state.Human_Treasure:
          
            Manhanthan_distances = dict.fromkeys(Solution[1])
            for i,state in enumerate(Solution[1]):
                print(f"{i} {state.Human_Treasure=}")
                print(f"{i} {state.Human_Pos=}")
                Manhanthan_distances[state]= ManhattanDistance(state.Human_Pos,state.Human_Treasure)
            
            Manhanthan_distances = dict(sorted(Manhanthan_distances.items(), key=lambda item: item[1]))	
            minHum = min(Manhanthan_distances.values())
            state = list(Manhanthan_distances.keys())[0]
            ExpandedNodes.append(state)
            #print(f"{hash(state)} -> {minHum=}")

    if len(ExpandedNodes)%1000 <= 1:
        print(len(ExpandedNodes),'nodes generated')
    if isAI:
        maxEval = -10**99

        for child in state.children_tileshift(isAI)[0]:
            if child.inList(ExpandedNodes):
                #print(f"already explored node: {hash(child)}, {state.side_tile} / {child.side_tile} / {turn=}")
                return maxEval
            else:
                ExpandedNodes.append(child)
            
            eval = minimax(child,turn+1, alpha, beta, False,state.Human_Treasure)
            if eval == None:continue
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        return maxEval
 
    else:
        minEval = 10**99

        for child in state.children_tileshift(isAI)[0]:
            if child.inList(ExpandedNodes):
                #print(f"already explored node: {hash(child)}, {state.side_tile} / {child.side_tile} /  {turn=}")
                return minEval
            else:
                ExpandedNodes.append(child)

            eval = minimax(child,turn+1, alpha, beta, True,state.Human_Treasure)
            if eval == None:continue
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
 
 
def alpha_beta_pruning_test(node, depth, alpha, beta, expandedNodes=[], isAI=True):
    if depth == 0 or node.isAI_at_goal() or node.isHuman_at_goal():
        eval = None
        if node.isAI_at_goal(): 
            print('solution found AI')
            eval = 1
        elif node.isHuman_at_goal():eval =-1
        else: eval = 1/ManhattanDistance(node.AI_Pos,node.AI_Treasure)
        return eval, None

    best_value = float('-inf') if isAI else float('inf')
    best_move = None
    children_dict = children_after_turn(node,isAI)

    if len(expandedNodes)%1000<=10:
        print(len(expandedNodes),'nodes generated')

    for child,moves in children_dict.items():
        
        if child not in expandedNodes:
            expandedNodes.append(child)
            value, _ = alpha_beta_pruning_test(child, depth-1, alpha, beta, expandedNodes, not isAI)

            if isAI and value > best_value:
                best_value, best_move = value, moves
                alpha = max(alpha, best_value)
            elif not isAI and value < best_value:
                best_value, best_move = value, moves
                beta  = min(beta, best_value)

            if beta <= alpha:
                print("Pruning",depth)
                break
        else:
            print("already expanded here")
    
    return best_value, best_move
