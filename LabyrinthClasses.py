from termcolor import colored
import copy
class State:
    def __init__(self, P1,P2,T1,T2,board):
        self.Human_Pos= P1
        self.AI_Pos = P2
        self.Human_Treasure = T1
        self.AI_Treasure = T2
        self.board = board
        self.size = (len(board),len(board[0]))
    def isGoal(self):
         if self.AI_Pos == self.AI_Treasure: return True
         else: return False
    def __str__(self):
        self.display()
    def childs(self):
        states = []
        for action in actions(self):
            states.append(results(self,action))
        return states
    
    def display(self):
        Board = [[] for _ in range(self.size[0])]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                Board[i].append(copy.deepcopy(self.board[i][j].ASCII))
        screen_rows = list()
    
        Board[self.Human_Treasure[0]][self.Human_Treasure[1]][1][1] = colored("$","blue")
        Board[self.AI_Treasure[0]][self.AI_Treasure[1]][1][1] = colored("£","red")
        
        Board[self.Human_Pos[0]][self.Human_Pos[1]][1][1] = colored("█","blue")
        Board[self.AI_Pos[0]][self.AI_Pos[1]][1][1] = colored("█","red")

        board_display = list()
        for row_nb in range(self.size[0]):
            for char_row in range(3):
                row = f"         ░{'░'.join([''.join(Board[row_nb][col][char_row]) for col in range(self.size[0])])}░"
                board_display.append(row)
            
            if row_nb != self.size[0]-1:
                board_display.append(f"         {(len(row)-9)*'░'}")

        screen_rows = ["","","","","",f"         {(len(row)-9)*'░'}"] + board_display + [f"         {(len(row)-9)*'░'}","","","","",""]

        for row in screen_rows:
            print(row)

class Action:
    def __init__(self, name, delta_row, delta_col):
        self.name = name
        self.delta_row = delta_row
        self.delta_col = delta_col
    def __str__(self):
        return self.name
        


#Définition des actions

MoveN = Action("MoveN",-1,0)
MoveS = Action("MoveS",1,0)
MoveE = Action("MoveE",0,-1)
MoveW = Action("MoveW",0,1)
ActionsList = [MoveN,MoveS,MoveE,MoveW]

class Tile:
    def __init__(self, name,OpenN,OpenE,OpenS,OpenW):
        self.name=name
        self.OpenN=OpenN
        self.OpenE=OpenE
        self.OpenS=OpenS
        self.OpenW=OpenW
        self.ASCII =[[" "," "," "],
			        [" ","█"," "],
			        [" "," "," "],]
        if OpenN : self.ASCII[0][1]="█"
        if OpenE : self.ASCII[1][2]="█"
        if OpenS : self.ASCII[2][1]="█"
        if OpenW : self.ASCII[1][0]="█"
    def __str__(self):
         return self.name
    

def results(state,action):
    #Returns the resulting state after applying the given action to the state
    result_Pos = [state.AI_Pos[0] + action.delta_row, state.AI_Pos[1]+action.delta_col]
    new_state = copy.deepcopy(state)
    new_state.AI_Pos=result_Pos
    return new_state

def actions(state):
    #Returns all the applicable actions for a given state
    applicableActions = []
    for action in ActionsList:
         if isApplicable(state,action): applicableActions.append(action)
    return applicableActions

def isApplicable(state,action):
    #Returns True if the action is applicable for the given state

    #Check if the action doesn't result in the AI going out of the board
    next_Pos = [state.AI_Pos[0] + action.delta_row, state.AI_Pos[1]+ action.delta_col]
    if -1 in next_Pos or state.size[0] in next_Pos: return False
    #Check if the action is applicable for current the tile
    tile_AI = state.board[state.AI_Pos[0]][state.AI_Pos[1]]

    if action.delta_row == -1:
          #MoveN
          if not tile_AI.OpenN: return False

    elif action.delta_row == 1:
          #MoveS
          if not tile_AI.OpenS: return False
    
    if action.delta_col == 1:
          #MoveE
          if not tile_AI.OpenE: return False
    
    elif action.delta_col == -1:
          #MoveW
          if not tile_AI.OpenW: return False

    #Check if the action is applicable for the next tile
    tile_Next = state.board[state.AI_Pos[0]+action.delta_row][state.AI_Pos[1]+action.delta_col]

    if action.delta_row == -1:
          #MoveN
          if not tile_Next.OpenS: return False

    elif action.delta_row == 1:
          #MoveS
          if not tile_Next.OpenN: return False
    
    if action.delta_col == 1:
          #MoveE
          if not tile_Next.OpenW: return False
    
    elif action.delta_col == -1:
          #MoveW
          if not tile_Next.OpenE: return False

    return True