from termcolor import colored
import copy
import numpy as np
from typing import Union
import random

class Entity:
    def __init__(self, x:int,y:int):
        self.x=x
        self.y=y
        
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Treasure(Entity):
    # Position is [-1,-1] if treasure is outside the board
    def __init__(self,x,y,id):
        super().__init__(x,y)
        self.id = id
        
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Player(Entity):
    def __init__(self,x,y, goal:Treasure, isAI:bool):
        super().__init__(x,y)
        self.goal = goal
        self.isAI=isAI
    
    def isAtGoal(self):
        return (self.x == self.goal.x and 
                self.y == self.goal.y)
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    


def generate_treasures(board_size,n):
    treasures = [0]*n
    for i in range(n):
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)
        while [x,y] in treasures:
            x = random.randint(0, board_size - 1)
            y = random.randint(0, board_size - 1)
        treasures[i]=Treasure(x,y,i)
    return treasures

treasures = generate_treasures(5,2)
AI = Player(0,0,treasures[0],True)
Human = Player(4,4,treasures[1],False)

class Tile:
    def __init__(self,OpenN:bool,OpenE:bool,OpenS:bool,OpenW:bool):
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
    

class State:
    def __init__(self, players:list[Player],treasures:list[Treasure],board:list,side_tile:Tile,forbidden_shift:Tile = None):
        self.players = players
        for p in players:
            if p.isAI:
                self.AI = p
                self.AI_Pos = [p.x,p.y]
                self.AI_Treasure = [p.goal.x,p.goal.y]
            else: 
                self.Human = p
                self.Human_Pos = [p.x,p.y]
                self.Human_Treasure = [p.goal.x,p.goal.y]
        self.treasures = treasures
        self.board = np.array(board)
        self.size = (len(board),len(board[0]))
        self.side_tile = side_tile
        self.forbidden_shift = forbidden_shift
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
            print('next to hash:')
            print(var)
            if key =='board':
                attributes.append(hash(tuple(map(tuple,var))))
            elif key == 'forbidden_shift' or key == 'side_tile' or key=='AI' or key == 'Human':
                attributes.append(hash(var))
            else: attributes.append(hash(tuple(var)))
        return hash(tuple(attributes))
    
    def isAI_at_goal(self):
         return self.AI_Pos == [self.AI.goal.x,self.AI.goal.y]
    def isHuman_at_goal(self):
         return self.Human_Pos == [self.Human.goal.x,self.Human.goal.y]
    def childs_move(self):
        states = []
        for action in actions(self,MoveAction):
            states.append(results(self,action))
        return states
    def inList(self,statesList: list):
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
    def __init__(self, name:str, delta_row:int, delta_col:int,isAI:bool=True):
        self.name = name
        self.delta_row = delta_row
        self.delta_col = delta_col
        self.isAI = isAI
    def __str__(self):
        return self.name
    
#Definition of moving actions
MoveN = MoveAction("MoveN",-1,0)
MoveS = MoveAction("MoveS",1,0)
MoveE = MoveAction("MoveE",0,-1)
MoveW = MoveAction("MoveW",0,1)
MoveActionsList_AI = [MoveN,MoveS,MoveE,MoveW]

MoveN = MoveAction("MoveN",-1,0,False)
MoveS = MoveAction("MoveS",1,0,False)
MoveE = MoveAction("MoveE",0,-1,False)
MoveW = MoveAction("MoveW",0,1,False)
MoveActionsList_Human = [MoveN,MoveS,MoveE,MoveW]


class TileShiftAction:
    def __init__(self,tile:Tile,isRowShift:bool,RowCol_index:int,direction:int):
        if RowCol_index % 2 == 1:
            #Only odd row/col indexes can be shifted
            self.new_tile = tile
            self.isRowShift = isRowShift
            self.index = RowCol_index
            self.dir = direction
        else: print("ERROR: Row/Col index must be odd")
    def __eq__(self,other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
    def __hash__(self):
        return hash(tuple(self.new_tiles),self.isRowShift,self.index,self.dir)
    def __str__(self):
        if self.isRowShift: row_or_col='row'
        else: row_or_col='column'
        return ('Tile '+str(self.new_tile) +' inserted at ' +row_or_col+str(self.index)+ ' in direction ' + str(self.dir))

    
def results(state,action:Union[TileShiftAction,MoveAction]):
    #Returns the resulting state after applying the given action to the state
    new_state = copy.deepcopy(state)

    if isinstance(action, MoveAction):
        if action.isAI: pos= state.AI_Pos
        else: pos = state.Human_Pos

        result_Pos = [pos[0] + action.delta_row, pos[1]+action.delta_col]

        if action.isAI: new_state.AI_Pos=result_Pos
        else: new_state.Human_Pos=result_Pos

    elif isinstance(action, TileShiftAction):
        #Shift tiles
        if action.isRowShift:
            line = state.board[action.index,:]
        else: line = state.board[:,action.index]

        if action.dir == 1 :
            new_state.side_tile, line = line[-1], line[:-1] 
            line = np.concatenate((np.array([action.new_tile]),line))
        else: 
            new_state.side_tile, line = line[0], line[1:]
            line = np.concatenate((line,np.array([action.new_tile])))
        
        if action.isRowShift:
            new_state.board[action.index,:] = line
        else: new_state.board[:,action.index] = line

        entities = new_state.players + new_state.treasures
        for entity in entities:
            if (action.isRowShift and entity.x == action.index) or (not action.isRowShift and entity.y == action.index):
                if action.isRowShift:
                    entity.y +=action.dir
                    if entity.y==state.size[0]:
                        if isinstance(entity,Player): entity.y=0
                        else: entity.y,entity.x = None,None
                    elif entity.y == -1 and isinstance(entity,Player):
                        entity.y=state.size[0]-1
                    else: entity.y,entity.x = None,None
                else: 
                    entity.x +=action.dir
                    if entity.x==state.size[0]:
                        if isinstance(entity,Player):
                            entity.x=0
                        else: entity.y,entity.x = None,None
                    elif entity.x == -1 and isinstance(entity,Player):
                        entity.x=state.size[0]-1
                    else: entity.y,entity.x = None,None
                print(entity.x,entity.y)
        new_state = State(new_state.players,new_state.treasures,new_state.board,new_state.side_tile,new_state.forbidden_shift)
        
    return new_state


def actions(state,actionClass:type,isAI:bool = True):

    #Returns all the applicable actions for a given state
    applicableActions = []
    if actionClass == MoveAction:
        if isAI: ActionsList = MoveActionsList_AI
        else: ActionsList = MoveActionsList_Human
        for action in ActionsList:
            if isApplicable(state,action): applicableActions.append(action)

    elif actionClass == TileShiftAction:
        forbidden_shift = state.forbidden_shift
        dirs = [-1,1]
        size = len(state.board)
        odd_indexes = [num for num in range(size) if num % 2 != 0]
        for dir in dirs:
            for index in odd_indexes:
                for isRowShift in [True,False]:
                    action = TileShiftAction(state.side_tile,isRowShift,index,dir)
                    applicableActions.append(action)
        if forbidden_shift in applicableActions : applicableActions.remove(forbidden_shift)

    return applicableActions



def isApplicable(state:State,action:MoveAction):
    #Returns True if the action is applicable for the given state

    #Check if the action doesn't result in the AI going out of the board
    if action.isAI: pos = state.AI_Pos
    else: pos = state.Human_Pos
    next_Pos = [pos[0] + action.delta_row, pos[1]+ action.delta_col]
    if -1 in next_Pos or state.size[0] in next_Pos: return False

    #Check if the action is applicable for current the tile
    tile = state.board[pos[0]][pos[1]]

    if action.delta_row == -1:
        #MoveN
        if not tile.OpenN: return False

    elif action.delta_row == 1:
        #MoveS
        if not tile.OpenS: return False
    
    if action.delta_col == 1:
        #MoveE
        if not tile.OpenE: return False
    
    elif action.delta_col == -1:
        #MoveW
        if not tile.OpenW: return False

    #Check if the action is applicable for the next tile
    tile_Next = state.board[pos[0]+action.delta_row][pos[1]+action.delta_col]

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
