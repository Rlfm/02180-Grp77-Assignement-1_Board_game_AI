import random

class Entity:
    def __init__(self, row:int,col:int):
        self.row=row
        self.col=col
        self.pos = (row,col)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Treasure(Entity):
    # Position is [None,None] if treasure is outside the board
    def __init__(self,row,col,id):
        super().__init__(row,col)
        self.id = id
        self.pos = (row,col)
        
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Player(Entity):
    def __init__(self,row,col, goal:Treasure, isAI:bool):
        super().__init__(row,col)
        self.goal = goal
        self.isAI=isAI
    
    def isAtGoal(self):
        return (self.row == self.goal.row and 
                self.col == self.goal.col)
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    

def generate_treasures(board_size,n):
    treasures = [0]*n
    for i in range(n):
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        while [row,col] in treasures:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - 1)
        treasures[i]=Treasure(row,col,i)
    return treasures

treasures = generate_treasures(5,2)
AI = Player(0,0,treasures[0],True)
Human = Player(4,4,treasures[1],False)


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
MoveW = MoveAction("MoveW",0,-1)
MoveE = MoveAction("MoveE",0,1)
MoveActionsList_AI = [MoveN,MoveS,MoveE,MoveW]

MoveN = MoveAction("MoveN",-1,0,False)
MoveS = MoveAction("MoveS",1,0,False)
MoveW = MoveAction("MoveW",0,-1,False)
MoveE = MoveAction("MoveE",0,1,False)
MoveActionsList_Human = [MoveN,MoveS,MoveE,MoveW]