import copy
import numpy as np
from typing import Union
from Entities import *
import logging
# termcolor is only needed for testing purposes
#from termcolor import colored

level = logging.INFO	
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level =level, format=fmt)

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
        return self.rotationsList()[i%4]
    
class State:
    def __init__(self, players:list[Player],treasures:list[Treasure],board:list,side_tile:Tile,forbidden_shift:Tile = None):
        self.players = players
        for p in players:
            if p.isAI:
                self.AI = p
                self.AI_Pos = [p.row,p.col]
                self.AI_Treasure = [p.goal.row,p.goal.col]
            else: 
                self.Human = p
                self.Human_Pos = [p.row,p.col]
                self.Human_Treasure = [p.goal.row,p.goal.col]
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
        logging.debug(self.__dict__)
        for key,var in self.__dict__.items():
            logging.debug('next to hash:')
            logging.debug(var)
            if key =='board':
                attributes.append(hash(tuple(map(tuple,var))))
            elif key == 'forbidden_shift' or key == 'side_tile' or key=='AI' or key == 'Human':
                attributes.append(hash(var))
            else: attributes.append(hash(tuple(var)))
        return hash(tuple(attributes))
    
    def isAI_at_goal(self):
         return self.AI_Pos == [self.AI.goal.row,self.AI.goal.col]
    def isHuman_at_goal(self):
         return self.Human_Pos == [self.Human.goal.row,self.Human.goal.col]
    def children_move(self,isAI:bool):
        states = []
        action_list =[]
        for action in actions(self,MoveAction,isAI):
            states.append(results(self,action))
            action_list.append(action)
        return states,action_list
    
    def children_tileshift(self,isAI:bool):
        states = []
        action_list = []
        for action in actions(self,TileShiftAction,isAI):
            states.append(results(self,action))
            action_list.append(action)
 
        return states, action_list
    

    def inList(self,statesList: list):
        for s in statesList:
              if s==self:
                   return True
        return False
    def treasure_positions(self):
        pos = []
        for t in self.treasures:
            pos.append([t.row,t.col])
        return pos
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
        
        screen_rows = ["","","","","",f"         {(len(row)-9)*'░'}"] + board_display + [f"         {(len(row)-9)*'░'}",""]
        
        for char_row in range(3):
                screen_rows.append(f"{round(len(board_display[0])/2+2)*' '} {''.join([self.side_tile.ASCII[char_row][col] for col in range(len(self.side_tile.ASCII[0]))])}")

        for row in screen_rows:
            print(row)

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
        if self.new_tile is not None:
            return hash((self.new_tile,self.isRowShift,self.index,self.dir))
        else: return hash((None,self.isRowShift,self.index,self.dir))
    def __str__(self):
        if self.isRowShift: row_or_col='row '
        else: row_or_col='column '
        return ('Tile '+str(self.new_tile) +' inserted at ' +row_or_col+str(self.index)+ ' in direction ' + str(self.dir))
    def is_forbidden(self,state:State):
        fs = state.forbidden_shift
        if (self.isRowShift==fs.isRowShift and
            self.index == fs.index and
            self.dir == fs.dir):
            return True
        else:
            return False

def results(state:State,action:Union[TileShiftAction,MoveAction]):
    #Returns the resulting state after applying the given action to the state
    new_state = copy.deepcopy(state)

    if isinstance(action, MoveAction):
        if action.isAI: pos= state.AI_Pos
        else: pos = state.Human_Pos

        result_Pos = [pos[0] + action.delta_row, pos[1]+action.delta_col]

        if action.isAI: new_state.AI.row,new_state.AI.col=result_Pos[0],result_Pos[1]
        else: new_state.Human.row,new_state.Human.col=result_Pos[0],result_Pos[1]
        
        assert new_state.Human_Treasure == state.Human_Treasure and new_state.AI_Treasure == state.AI_Treasure
    
    elif isinstance(action, TileShiftAction):
        # Shift tiles
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

        # Shift entities
        entities = new_state.players + new_state.treasures
        for entity in entities:
            if (action.isRowShift and entity.row == action.index) or (not action.isRowShift and entity.col == action.index):
                if action.isRowShift:
                    entity.col +=action.dir
                    if entity.col==state.size[0]:
                        if isinstance(entity,Player): entity.col=0
                        else: entity.row,entity.col = None,None
                    elif entity.col == -1:
                        if isinstance(entity,Player): entity.col=state.size[0]-1
                        else: entity.row,entity.col = None,None
                else: 
                    entity.row +=action.dir
                    if entity.row==state.size[0]:
                        if isinstance(entity,Player):
                            entity.row=0
                        else: entity.row,entity.col = None,None
                    elif entity.row == -1:
                        if isinstance(entity,Player): entity.row=state.size[0]-1
                        else: entity.row,entity.col = None,None
                #print(entity.row,entity.col)
            elif isinstance(entity, Treasure) and entity.row == None:
                if action.isRowShift:
                    if action.dir == 1:
                        entity.row,entity.col = action.index,0
                    else:
                        entity.row,entity.col = action.index,state.size[0]-1
                else:
                    if action.dir == 1:
                        entity.row,entity.col = 0, action.index
                    else: 
                        entity.row,entity.col = state.size[0]-1, action.index
        
        # Update the forbidden shift
        new_state.forbidden_shift = TileShiftAction(new_state.side_tile,action.isRowShift,action.index,-action.dir)

    return State(new_state.players,new_state.treasures,new_state.board,new_state.side_tile,new_state.forbidden_shift)

def results_list(state:State,action_list):
    resulting_state = state
    for action in action_list:
        resulting_state = results(resulting_state,action)
    return resulting_state


def actions(state:State,actionClass:type,isAI:bool):

    #Returns all the applicable actions for actionClass type for a given state
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
                    if forbidden_shift is None or not(dir == forbidden_shift.dir and 
                           index == forbidden_shift.index and 
                           isRowShift == forbidden_shift.isRowShift): 
                        if str(state.side_tile) == "1010" or str(state.side_tile) == "0101":
                            for i in range(2):
                                action = TileShiftAction(state.side_tile.rotate(i),isRowShift,index,dir)
                                applicableActions.append(action)
                        else:
                            for i in range(4):
                                action = TileShiftAction(state.side_tile.rotate(i),isRowShift,index,dir)
                                applicableActions.append(action)
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

