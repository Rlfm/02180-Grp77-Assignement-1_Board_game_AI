from collections import deque
from Entities import *
from States import *

def bfs_search(start_state,isAI):

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
        
        # Check if we've found the goal state
        if node.isAI_at_goal() or node.isHuman_at_goal():
            return  (path[node],expandedNodes)
        
        # Add child nodes to the queue if they haven't been visited
        
        for child in node.childs_move(isAI):
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
    # If we haven't found the goal state, return None
    return (None,expandedNodes)

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
        
        for child in node.childs_move(isAI):
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
    # If we haven't found the goal state, return None
    return expandedNodes

#TODO: Finish the manhattan heuristic calculation
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
            Manhanthan_distances = list()
            for state in bfs_solution[1]:
                Manhanthan_distances.append(ManhattanDistance(state.AI_Pos,state.AI_Treasure))
            minAI = min(Manhanthan_distances)
        print(f"{minAI=}")

        if bfs_solution[0] != None:
            del heuristic_TileShift[i]
            continue   

        else: # Calculate Manhatan distance for P1 to all Treasures 
            Manhanthan_distances = list()
            for potential_treasure in [x for x in start_state.treasures if x != start_state.AI_Treasure]:
                pos = (potential_treasure.row, potential_treasure.col)
                for state in bfs_search(Potential_state,False)[1]:
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