from collections import deque

def bfs_search(start_state):

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
        if node.isGoal():
            return  (path[node],expandedNodes)
        
        # Add child nodes to the queue if they haven't been visited
        
        for child in node.childs_move():
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
    # If we haven't found the goal state, return None
    return (None,expandedNodes)

#TODO: Finish the manhattan heuristic calculation
def ManhattanHeuristic(state):
    row = state.AI_Pos[0]
    col = state.AI_Pos[1]
    goal_row = state.AI_Treasure[0]
    goal_col = state.AI_Treasure[0]

    return abs(row-goal_row) + abs(col-goal_col)