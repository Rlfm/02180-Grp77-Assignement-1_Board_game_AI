from termcolor import colored
import copy


class State:
    def __init__(self, P1,P2,T1,T2,board,side_tiles):
        self.Human_Pos= P1
        self.AI_Pos = P2
        self.Human_Treasure = T1
        self.AI_Treasure = T2
        self.board = board
        self.size = (len(board),len(board[0]))
        self.side_tiles = side_tiles
        #self.turn
        #self.forbiddenShift
    def isGoal(self):
         if self.AI_Pos == self.AI_Treasure: return True
         else: return False
    def __str__(self):
        self.display()
    def __eq__(self,other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
    def __hash__(self):
        attributes = []
        print(self.__dict__)
        for key,var in self.__dict__.items():
            print(var)
            if key=='board':
                attributes.append(hash(tuple(map(tuple,var))))
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
    def __init__(self,tiles,isRowShift,RowCol_index,direction):
        if RowCol_index % 2 == 1:
            #Only odd row/col indexes can be shifted
            self.new_tiles=tiles
            self.isRowShift = isRowShift
            self.index = RowCol_index
            self.dir =direction
        else: print("ERROR: Row/Col index must be odd")

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
            #line = state.board[action.index]
            new_tiles_number = len(action.new_tiles)
            for tile in action.new_tiles:
                new_state.side_tiles.remove(tile) 
                pass
            if action.dir==1:
                for i in range(new_tiles_number):
                    new_state.side_tiles.append(state.board[action.index][state.size[0]-i-1])
            else:
                for i in range(new_tiles_number):
                    new_state.side_tiles.append(state.board[action.index][i])

            if action.dir==1:
                for i in range(state.size[0]-new_tiles_number):

                    new_state.board[action.index][state.size[0]-i-1] = state.board[action.index][state.size[0]-i-2]
                for i in range(new_tiles_number):
                    new_state.board[action.index][i] = action.new_tiles[i]
            else:
                for i in range(state.size[0]-new_tiles_number):
                    new_state.board[action.index][i] = state.board[action.index][i+1]
                for i in range(new_tiles_number):
                    new_state.board[action.index][state.size[0]-i-1] = action.new_tiles[-1-i]
    return new_state

#TODO: Add support for TileShiftActions
def actions(state,action):
    #Returns all the applicable actions for a given state
    applicableActions = []
    if isinstance(action,MoveAction):
        for action in MoveActionsList:
            if isApplicable(state,action): applicableActions.append(action)
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