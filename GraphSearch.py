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
        if node.isAI_at_goal():
            return  (path[node],expandedNodes)
        
        # Add child nodes to the queue if they haven't been visited
        
        for child in node.childs_move():
            if not child.inList(frontier) and not child.inList(expandedNodes):
                frontier.append(child)
                path[child] = path[node] + [child]
    # If we haven't found the goal state, return None
    return (None,expandedNodes)

#TODO: Finish the manhattan heuristic calculation
def ManhattanDistance(Pos1,Pos2):
    row = Pos1[0]
    col = Pos1[1]
    goal_row = Pos1[0]
    goal_col = Pos1[1]
    return abs(row-goal_row) + abs(col-goal_col)


def A_star(start_state):

    start_state.side_tile