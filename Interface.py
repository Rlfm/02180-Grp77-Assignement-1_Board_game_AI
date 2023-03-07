import pygame
from States import *
import random
import copy
import time
from GraphSearch import *

# Initialize Pygame
pygame.init()

MARGIN = 50
DASHBOARD = 200
TILE_SIDE = 100
ROWS = 7
COLS = 7

BLUE = (47, 60, 113)
RED = (230,0,0)
GRAY = (180,180,180)
YELLOW = (255,240,46)
FONT = pygame.font.Font(None, 36)  # None means use the default font; 36 is the font size

# Set the size of the game SCREEN
SCREEN_WIDTH = TILE_SIDE*COLS+2*MARGIN+DASHBOARD
SCREEN_HEIGHT = TILE_SIDE*ROWS+2*MARGIN
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SIDE_TILE_X = MARGIN*2+TILE_SIDE*COLS+DASHBOARD/2
SIDE_TILE_Y = TILE_SIDE

# TEXT

TEXT_X_CENTER = SCREEN_WIDTH - DASHBOARD/2
TEXT_Y_CENTER = TILE_SIDE*3
TEXT_TURN = ["AI's turn ...", "Your turn !"]
COLORS = [GRAY,RED]

# Set the size of each tile
tile_width = TILE_SIDE
tile_height = TILE_SIDE

arrow_height = TILE_SIDE/3
arrow_width = arrow_height/2

ROT_WIDTH = TILE_SIDE/2
ROT_HEIGHT = ROT_WIDTH/2

ROT_1_X = SCREEN_WIDTH-DASHBOARD/2-TILE_SIDE/2
ROT_2_X = ROT_1_X+ROT_WIDTH
ROT_Y = SIDE_TILE_Y+TILE_SIDE

side_tile_rot = 0
Human_Turn = True

# Load the sprite images
TILE_IMAGES_RAW = {
    'corner':pygame.image.load('sprites/Tile_Corner.png').convert_alpha(),
    'straight':pygame.image.load('sprites/Tile_Straight.png').convert_alpha(),
    'T':pygame.image.load('sprites/Tile_T.png').convert_alpha()}


# Create an image dictionnary
TILE_IMAGES ={}

# Create rotated versions of each tile image and add them to the appropriate sprite groups
for tile_name, tile_image in TILE_IMAGES_RAW.items():

    tile_image = pygame.transform.scale(tile_image,(tile_width,tile_height))
    if tile_name == 'straight':
        # Straight tile has only 2 possible rotations
        for i in range(2):
            rotated_image = pygame.transform.rotate(tile_image, i*-90)
            TILE_IMAGES[Tile(1,0,1,0).rotate(i)] = rotated_image
    else:
        # All other tiles have 4 possible rotations
        for i in range(4):
            rotated_image = pygame.transform.rotate(tile_image, i*-90)
            if tile_name == 'corner':
                TILE_IMAGES[Tile(0,1,1,0).rotate(i)] = rotated_image
            elif tile_name == 'T':
                TILE_IMAGES[Tile(1,1,1,0).rotate(i)] = rotated_image

BOARD_SPRITES = [[pygame.sprite.Sprite() for j in range(COLS)] for i in range(ROWS)]
for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect(MARGIN+TILE_SIDE*j,MARGIN+TILE_SIDE*i,TILE_SIDE,TILE_SIDE)
        BOARD_SPRITES[i][j].rect = rect

SIDE_TILE_SPRITE = pygame.sprite.Sprite()
SIDE_TILE_SPRITE.rect=pygame.Rect(SIDE_TILE_X-TILE_SIDE/2,SIDE_TILE_Y-TILE_SIDE/2,TILE_SIDE-SIDE_TILE_X/2,TILE_SIDE-SIDE_TILE_Y/2)

# Load treasure images
treasure_images = [pygame.image.load('sprites/treasure0.png').convert_alpha(),
                   pygame.image.load('sprites/treasure1.png').convert_alpha(),
                   pygame.image.load('sprites/treasure2.png').convert_alpha()]

treasure_sprites = [0]*len(treasure_images)

for i in range(len(treasure_images)):
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(treasure_images[i],(TILE_SIDE/2.5,TILE_SIDE/2.5))
    sprite.rect = sprite.image.get_rect()
    treasure_sprites[i] = sprite

def blitTreasures(treasures:list[Treasure]):
    for treasure in treasures:
        sprite = treasure_sprites[treasure.id]
        if treasure.row == None:
            sprite.rect.center = (SIDE_TILE_X,SIDE_TILE_Y)
        else: 
            sprite.rect.center = (MARGIN+TILE_SIDE*(treasure.col+0.5),MARGIN+TILE_SIDE*(treasure.row+0.5))
        SCREEN.blit(sprite.image,sprite.rect)

# Load player images
player_images = [pygame.image.load('sprites/player1.png').convert_alpha(),
                   pygame.image.load('sprites/player2.png').convert_alpha()]

PLAYER_SPRITES={}
for i in range(len(player_images)):
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(player_images[i],(TILE_SIDE/2.5,TILE_SIDE/2.5))
    sprite.rect = sprite.image.get_rect()
    PLAYER_SPRITES[i] = sprite

def blitPlayers(players:list[Player]):
    for player in players:
        if player.isAI: sprite = PLAYER_SPRITES[0]
        else: sprite = PLAYER_SPRITES[1]
        sprite.rect.center = (MARGIN+TILE_SIDE*(player.col+0.5),MARGIN+TILE_SIDE*(player.row+0.5))

    if PLAYER_SPRITES[0].rect.center == PLAYER_SPRITES[1].rect.center:
        PLAYER_SPRITES[0].rect.x = PLAYER_SPRITES[0].rect.x-TILE_SIDE/7
        PLAYER_SPRITES[1].rect.x = PLAYER_SPRITES[1].rect.x+TILE_SIDE/7
    SCREEN.blit(PLAYER_SPRITES[0].image,PLAYER_SPRITES[0].rect)
    SCREEN.blit(PLAYER_SPRITES[1].image,PLAYER_SPRITES[1].rect)


# Load shifting arrows sprites
ARROW_IMAGES = [pygame.transform.scale(pygame.image.load('sprites/arrow_unavailable.png').convert_alpha(),(arrow_width,arrow_height)),
                pygame.transform.scale(pygame.image.load('sprites/arrow.png').convert_alpha(),(arrow_width,arrow_height))]
odds = [num for num in range(ROWS) if num % 2 != 0]
ARROW_SPRITES = [[[pygame.sprite.Sprite() for _ in range(4)] for _ in range(len(odds))] for _ in range(2)]
for i in range(4): #All rotations
    for j in range(len(odds)): #All indexes
        for k in range(2): #Available/Unavailable
            rotated_image = pygame.transform.rotate(ARROW_IMAGES[k], i*-90)

            sprite = pygame.sprite.Sprite()
            sprite.image = rotated_image
            sprite.rect = rotated_image.get_rect()

            if i%2==0:
                sprite.rect.center = (MARGIN*(i+1)/2+(i/2)*COLS*TILE_SIDE, MARGIN+(j*2+1+.5)*TILE_SIDE)
            else:
                sprite.rect.center = (MARGIN+(j*2+1+.5)*TILE_SIDE, MARGIN*(i)/2+((i-1)/2)*ROWS*TILE_SIDE)
            ARROW_SPRITES[k][j][i] = sprite


# Display the arrows, side after side
def blitArrows(state:State):
    forbidden_shift = state.forbidden_shift
    if forbidden_shift is not None:
        j=[i for i in range(4)]
        odds = [num for num in range(4) if num % 2 != 0]
        evens = [num for num in range(4) if num % 2 == 0]
        if not forbidden_shift.isRowShift: 
            for even in evens:
                j.remove(even)
            if forbidden_shift.dir != 1:
                j=j[-1]
            else: j = j[0]
        else :
            for odd in odds:
                j.remove(odd)
            if forbidden_shift.dir == 1:
                j = j[0]
            else: 
                j =j[-1]
        i = int((forbidden_shift.index-1)/2)
    else: i,j=-1,-1
    for k in range(len(ARROW_SPRITES[0])):
        for m in range(len(ARROW_SPRITES[0][0])):
            sprite = ARROW_SPRITES[not (k==i and m==j)][k][m]
            SCREEN.blit(sprite.image,sprite.rect)
    

# Load rotating arrows sprites
ROT_IMAGES = [pygame.transform.scale(pygame.image.load('sprites/arrow_rot_unavailable.png').convert_alpha(),(ROT_WIDTH,ROT_HEIGHT)),
              pygame.transform.scale(pygame.image.load('sprites/arrow_rot.png').convert_alpha(),(ROT_WIDTH,ROT_HEIGHT))]
ROT_SPRITES=[[pygame.sprite.Sprite() for i in range(2)] for i in range(2)]
for i in range(2):
    for j in range(2):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.flip(ROT_IMAGES[i], not j, False)
        sprite.rect = pygame.Rect(ROT_1_X*(not j) + ROT_2_X*j,ROT_Y,ROT_WIDTH,ROT_HEIGHT)
        ROT_SPRITES[i][j]=sprite

# Display the rotating arrows
def blitRot(available):
    for i in range(2):
        SCREEN.blit(ROT_SPRITES[available][i].image,ROT_SPRITES[available][i].rect)

def fill_board_sprites(board,tile_sprites,tile_images):
    w,h = len(board),len(board[0])
    for i in range(w):
        for j in range(h):
            tile_sprites[i][j].image = tile_images[board[i][j]]
    return tile_sprites

def blitText():
    text = FONT.render(TEXT_TURN[Human_Turn], True, COLORS[Human_Turn])  # True means to use anti-aliasing; (255, 255, 255) is the color
    text_rect = text.get_rect()
    text_rect.centerx = TEXT_X_CENTER
    text_rect.centery = TEXT_Y_CENTER
    SCREEN.blit(text, text_rect)



Displayed_State = None
def display_state(state:State):

    SCREEN.fill(BLUE)

    # Blit Board

    global Displayed_State
    Displayed_State=state
    fill_board_sprites(state.board,BOARD_SPRITES,TILE_IMAGES)
    for i in range(len(BOARD_SPRITES)):
        for j in range(len(BOARD_SPRITES[0])):
            SCREEN.blit(BOARD_SPRITES[i][j].image,BOARD_SPRITES[i][j].rect)

    # Blit the side tile
    if state.side_tile is not None : 
        SIDE_TILE_SPRITE.image = TILE_IMAGES[state.side_tile]
        SCREEN.blit(SIDE_TILE_SPRITE.image,SIDE_TILE_SPRITE.rect)

    # Blit entities
    blitTreasures(state.treasures)
    blitPlayers(state.players)

    #Blit the arrows
    blitArrows(state)

    # Blit the rot arrows
    blitRot(Human_Turn)

    blitText()

    pygame.display.update()


def display_state_sequence(states:list[State]):
    for s in states:
        display_state(s)
        time.sleep(0.5)

def handle_rot_click(event):
    global side_tile_rot
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        if ROT_SPRITES[1][0].rect.collidepoint(mouse_pos):
            Displayed_State.side_tile = Displayed_State.side_tile.rotate(-1)
        elif ROT_SPRITES[1][1].rect.collidepoint(mouse_pos):
            Displayed_State.side_tile = Displayed_State.side_tile.rotate(-1)

def handle_arrow_click(event):
    global side_tile_rot
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for rot in range(4):
            for index in range(len(odds)):
                if ARROW_SPRITES[1][index][rot].rect.collidepoint(mouse_pos):

                    if rot%2 == 1 : isRowShift = 0
                    else: isRowShift = 1
                    if rot<2: dir = 1
                    else: dir = -1

                    if Displayed_State.forbidden_shift is None or not(Displayed_State.forbidden_shift.isRowShift == isRowShift and
                           Displayed_State.forbidden_shift.index == index*2+1 and
                           Displayed_State.forbidden_shift.dir == dir):
                        return TileShiftAction(Displayed_State.side_tile.rotate(side_tile_rot),isRowShift,index*2+1,dir)
        return None

def handle_tile_click(event):
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(ROWS):
            for j in range(ROWS):
                if BOARD_SPRITES[i][j].rect.collidepoint(mouse_pos):
                    states = bfs_search_no_goal(Displayed_State,False)
                    for s in states:
                        if s.Human_Pos == [i,j]:
                            print("Approachable")
                            return True
        return False
                        
                    
##TESTING

Corner1 = Tile(0,1,1,0)
Corner2 = Tile(1,1,0,0)
Corner3 = Tile(1,0,0,1)
Corner4 = Tile(0,0,1,1)
T_1 = Tile(1,1,1,0)
T_2 = Tile(1,1,0,1)
T_3 = Tile(1,0,1,1)
T_4 = Tile(0,1,1,1)
Straight1 = Tile(1,0,1,0)
Straight2 = Tile(0,1,0,1)

'''5x5
CurrentTiles = [[copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_2),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Straight1),copy.deepcopy(T_4),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_2)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_3),copy.deepcopy(Straight1)],
		[copy.deepcopy(Corner2),copy.deepcopy(Corner4),copy.deepcopy(Corner1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight2),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],]
'''

CurrentTiles = [[copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_2),copy.deepcopy(T_3),copy.deepcopy(T_4),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Straight1),copy.deepcopy(T_4),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_2),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_3),copy.deepcopy(Straight1),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Corner2),copy.deepcopy(T_3),copy.deepcopy(Corner1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Corner1),copy.deepcopy(T_2),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_3),copy.deepcopy(T_4)],
        [copy.deepcopy(Straight1),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_3),copy.deepcopy(T_4)],
        [copy.deepcopy(Straight1),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_3),copy.deepcopy(T_4)]]

forbidden_shift = None

Treasure_P1 = Treasure(6,0,0)
Treasure_P2 = Treasure(3,1,1)
treasures = [Treasure_P1,Treasure_P2]

AI = Player(0,0,treasures[0],True)
Human = Player(1,1,treasures[1],False)

test_state = State([AI,Human],treasures,CurrentTiles,Tile(0,0,1,1),forbidden_shift)
Solution = bfs_search(test_state,True)


# Update the display
pygame.display.update()



def main():
    global Human_Turn
    global test_state
    blitRot(True)
    Human_Turn = False
    display_state(test_state)
    time.sleep(1)
    display_state_sequence(Solution[0])
    blitRot(Human_Turn)
    pygame.display.update()
    Human_Turn=True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_rot_click(event)
            tile_shift = handle_arrow_click(event)
            if tile_shift is not None:
                test_state = results(test_state,tile_shift)
            handle_tile_click(event)

        display_state(test_state)
        pygame.display.update()

if __name__=="__main__":
    main()