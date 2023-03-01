from termcolor import colored
import copy
import numpy as np

class State:
    def __init__(self, P1,P2,T1,T2,board,side_tile,forbidden_shift = None):
        self.Human_Pos= P1
        self.AI_Pos = P2
        self.Human_Treasure = T1
        self.AI_Treasure = T2
        self.board = np.array(board)
        self.size = (len(board),len(board[0]))
        self.side_tile = side_tile
        self.forbidden_shift = forbidden_shift
    def isGoal(self):
         if self.AI_Pos == self.AI_Treasure: return True
         else: return False
    def __str__(self):
        self.display()
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.Human_Pos == other.Human_Pos and
                    self.AI_Pos == other.AI_Pos and
                    self.Human_Treasure == other.Human_Treasure and
                    self.AI_Treasure == other.AI_Treasure and
                    np.array_equal(self.board, other.board) and
                    self.size == other.size and
                    self.side_tile == other.side_tile and
                    self.forbidden_shift == other.forbidden_shift)
        else:
            return False
    def __hash__(self):
        attributes = []
        print(self.__dict__)
        for key,var in self.__dict__.items():
            print(var)
            if key =='board':
                attributes.append(hash(tuple(map(tuple,var))))
            elif key == 'forbidden_shift':
                attributes.append(hash(var))
            else: attributes.append(hash(tuple(var)))
        return hash(tuple(attributes))
    def childs_move(self):
        states = []
        for action in actions(self,MoveAction):
            states.append(results(self,action))
        return states
    def inList(self,statesList):
        for s in statesList:
              if s==self:
                   return True
        return False
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

class MoveAction:
    def __init__(self, name, delta_row, delta_col):
        self.name = name
        self.delta_row = delta_row
        self.delta_col = delta_col
    def __str__(self):
        return self.name
    
#Definition of moving actions
MoveN = MoveAction("MoveN",-1,0)
MoveS = MoveAction("MoveS",1,0)
MoveE = MoveAction("MoveE",0,-1)
MoveW = MoveAction("MoveW",0,1)
MoveActionsList = [MoveN,MoveS,MoveE,MoveW]

class TileShiftAction:
    def __init__(self,tile,isRowShift,RowCol_index,direction):
        if RowCol_index % 2 == 1:
            #Only odd row/col indexes can be shifted
            self.new_tile=tile
            self.isRowShift = isRowShift
            self.index = RowCol_index
            self.dir =direction
        else: print("ERROR: Row/Col index must be odd")
    def __eq__(self,other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
    def __hash__(self):
        return hash(tuple(self.new_tiles),self.isRowShift,self.index,self.dir)

class Tile:
    def __init__(self,OpenN,OpenE,OpenS,OpenW):
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
         return str(self.OpenN)+str(self.OpenE)+str(self.OpenS)+str(self.OpenW)
    def __eq__(self,tile):
        return self.OpenN==tile.OpenN and self.OpenE==tile.OpenE and self.OpenS==tile.OpenS and self.OpenW==tile.OpenW
    def __hash__(self):
        return hash((self.OpenN,self.OpenE,self.OpenS,self.OpenW))
    
    def rotationsList(self):
        #Function returning all possible tiles by rotating a given tile
        tilesList =[copy.deepcopy(self) for i in range(4)]
        tilesList[1] = Tile(self.OpenW,self.OpenN,self.OpenE,self.OpenS)
        tilesList[2] = Tile(self.OpenS,self.OpenW,self.OpenN,self.OpenE)
        tilesList[3] = Tile(self.OpenE,self.OpenS,self.OpenW,self.OpenN)
        return tilesList
    def rotate(self,i):
        return self.rotationsList()[i]
    
def results(state,action):
    #Returns the resulting state after applying the given action to the state
    new_state = copy.deepcopy(state)
    if isinstance(action, MoveAction):
        result_Pos = [state.AI_Pos[0] + action.delta_row, state.AI_Pos[1]+action.delta_col]
        new_state.AI_Pos=result_Pos
    #TODO: add support for column shift
    elif isinstance(action, TileShiftAction):
        if action.isRowShift:
            line = state.board[action.index,:]
        else: line = state.board[:,action.index]

        if action.dir == 1 :
            new_state.side_tile, line = line[-1], line[:-1] 
            line = np.concatenate((action.new_tile,line))
        else: 
            new_state.side_tile, line = line[0], line[1:]
            line = np.concatenate((line,action.new_tile))
        
        if action.isRowShift:
            new_state.board[action.index,:] = line
        else: new_state.board[:,action.index] = line

        new_state.board
    return new_state


def subsets(lst):
    if len(lst) == 0:
        return [[]]
    smaller = subsets(lst[:-1])
    extra = lst[-1:]
    new = []
    for small in smaller:
        new.append(small+extra)
    return smaller+new

def actions(state,actionClass):

    #Returns all the applicable actions for a given state
    applicableActions = []

    if actionClass == MoveAction:
        for action in MoveActionsList:
            if isApplicable(state,action): applicableActions.append(action)

    elif actionClass == TileShiftAction:
        forbiddenShift = state.forbiddenShift
        dirs = [-1,1]
        size = len(state.board)
        odd_indexes = [num for num in range(size) if num % 2 != 0]
        tiles = state.side_tiles
        for subset in subsets(tiles):
            for dir in dirs:
                for index in odd_indexes:
                    for isRowShift in [True,False]:
                        action = TileShiftAction(subset,isRowShift,index,dir)
                        applicableActions.append(action)
        applicableActions.remove(forbiddenShift)

    return applicableActions



def isApplicable(state,action):
    #Returns True if the action is applicable for the given state

    if isinstance(action, MoveAction):

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
    
    else: print('HAS TO BE A MOVEACTION OBJECT')