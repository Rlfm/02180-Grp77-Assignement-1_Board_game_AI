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
BLUE = (47, 60, 113)
LIGHT_BLUE =(0,0,255)
RED = (230,0,0)
GRAY = (180,180,180)
YELLOW = (255,240,46)
GREEN = (0,255,0)
FONT_TURN = pygame.font.Font(None, 36)  # None means use the default font; 36 is the font size
FONT_INSTRUCTIONS = pygame.font.Font(None,28)
FONT_AGAIN = pygame.font.Font(None,36)
FONT_TREASURE = pygame.font.Font(None,30)
WaitingShift=False
WaitingMove = False
pygame.display.set_caption("LABYRINTH")

def init_game(rows,cols):
    global ROWS
    global COLS
    global SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN, SIDE_TILE_X,SIDE_TILE_Y,TEXT_X_CENTER,TEXT_Y_CENTER
    global tile_height,tile_width, arrow_height,arrow_width, ROT_WIDTH,ROT_HEIGHT,ROT_1_X,ROT_2_X,ROT_Y
    global TEXT_TURN,COLORS, TILE_IMAGES, odds,side_tile_rot,AUDIO_DICT,TEXT_INSTRUCTIONS
    global INSTRUCT_X_CENTER,INSTRUCT_Y_CENTER, TEXT_TREASURE,GOAL_TEXT_X_CENTER,GOAL_TEXT_Y_CENTER
    global GOAL_X_CENTER,GOAL_Y_CENTER, AGAIN_SPRITE
    ROWS = rows
    COLS = cols

    SCREEN_WIDTH = TILE_SIDE*COLS+2*MARGIN+DASHBOARD
    SCREEN_HEIGHT = TILE_SIDE*ROWS+2*MARGIN
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    


    TEXT_X_CENTER = SCREEN_WIDTH - DASHBOARD/2
    TEXT_Y_CENTER = TILE_SIDE/2

    INSTRUCT_X_CENTER = SCREEN_WIDTH - DASHBOARD/2
    INSTRUCT_Y_CENTER = TEXT_Y_CENTER+TILE_SIDE/3

    SIDE_TILE_X = MARGIN*2+TILE_SIDE*COLS+DASHBOARD/2
    SIDE_TILE_Y = INSTRUCT_Y_CENTER+2*TILE_SIDE/3
    
    tile_width = TILE_SIDE
    tile_height = TILE_SIDE

    arrow_height = TILE_SIDE/3
    arrow_width = arrow_height/2

    ROT_WIDTH = TILE_SIDE/2
    ROT_HEIGHT = ROT_WIDTH/2

    ROT_1_X = SCREEN_WIDTH-DASHBOARD/2-TILE_SIDE/2
    ROT_2_X = ROT_1_X+ROT_WIDTH
    ROT_Y = SIDE_TILE_Y+TILE_SIDE/1.5

    GOAL_X_CENTER = SCREEN_WIDTH-DASHBOARD/2
    GOAL_Y_CENTER = TILE_SIDE*4
    GOAL_TEXT_X_CENTER = SCREEN_WIDTH-DASHBOARD/2
    GOAL_TEXT_Y_CENTER = GOAL_Y_CENTER-TILE_SIDE/2

    AGAIN_X_CENTER = SCREEN_WIDTH-DASHBOARD/2
    AGAIN_Y_CENTER = GOAL_Y_CENTER+TILE_SIDE
    TEXT_TURN = ["AI's turn ...", "Your turn !", "AI Won :(","You won !!"]
    TEXT_INSTRUCTIONS =["Slide the tile",'Move your pawn']
    TEXT_TREASURE = "Your  treasure:"
    COLORS = [GRAY,LIGHT_BLUE,RED,GREEN]

    # Set the size of each tile


    side_tile_rot = 0

    global Human_Turn
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
    global BOARD_SPRITES
    BOARD_SPRITES = [[pygame.sprite.Sprite() for j in range(COLS)] for i in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(MARGIN+TILE_SIDE*j,MARGIN+TILE_SIDE*i,TILE_SIDE,TILE_SIDE)
            BOARD_SPRITES[i][j].rect = rect
    global SIDE_TILE_SPRITE
    SIDE_TILE_SPRITE = pygame.sprite.Sprite()
    SIDE_TILE_SPRITE.rect=pygame.Rect(SIDE_TILE_X-TILE_SIDE/2,SIDE_TILE_Y-TILE_SIDE/2,TILE_SIDE-SIDE_TILE_X/2,TILE_SIDE-SIDE_TILE_Y/2)

    # Load treasure images
    treasure_images = [pygame.image.load('sprites/treasure0.png').convert_alpha(),
                    pygame.image.load('sprites/treasure1.png').convert_alpha(),
                    pygame.image.load('sprites/treasure2.png').convert_alpha()]
    global treasure_sprites
    treasure_sprites = [0]*len(treasure_images)

    for i in range(len(treasure_images)):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(treasure_images[i],(TILE_SIDE/2.5,TILE_SIDE/2.5))
        sprite.rect = sprite.image.get_rect()
        treasure_sprites[i] = sprite


    # Load player images
    player_images = [pygame.image.load('sprites/player1.png').convert_alpha(),
                    pygame.image.load('sprites/player2.png').convert_alpha()]
    global PLAYER_SPRITES
    PLAYER_SPRITES={}
    for i in range(len(player_images)):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(player_images[i],(TILE_SIDE/2.5,TILE_SIDE/2.5))
        sprite.rect = sprite.image.get_rect()
        PLAYER_SPRITES[i] = sprite



    global ARROW_SPRITES
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

    global ROT_SPRITES
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
    AGAIN_IMAGE = pygame.transform.scale(pygame.image.load('sprites/play_again.png').convert_alpha(),(200,100))
    sprite = pygame.sprite.Sprite()
    sprite.image = AGAIN_IMAGE
    sprite.rect = pygame.Rect(AGAIN_X_CENTER,AGAIN_Y_CENTER,200,100)
    sprite.rect.center = (AGAIN_X_CENTER,AGAIN_Y_CENTER)
    AGAIN_SPRITE = sprite
    
    AUDIO_DICT ={'AIready' : pygame.mixer.Sound('audio/AIready.wav'),
                 'HumanLost': pygame.mixer.Sound('audio/HumanLost.wav'),
                 'HumanTurn': pygame.mixer.Sound('audio/HumanTurn.wav'),
                 'HumanWon': pygame.mixer.Sound('audio/HumanWon.wav'),
                 'PlayerMove': pygame.mixer.Sound('audio/PlayerMove.wav'),
                 'TileShift': pygame.mixer.Sound('audio/TileShift.wav')}


def blitTreasures(treasures:list[Treasure]):
    for treasure in treasures:
        sprite = treasure_sprites[treasure.id]
        if treasure.row == None:
            sprite.rect.center = (SIDE_TILE_X,SIDE_TILE_Y)
        else: 
            sprite.rect.center = (MARGIN+TILE_SIDE*(treasure.col+0.5),MARGIN+TILE_SIDE*(treasure.row+0.5))
        SCREEN.blit(sprite.image,sprite.rect)
        if Displayed_State.Human.goal==treasure:
            sprite.rect.center = (GOAL_X_CENTER,GOAL_Y_CENTER)
            image = pygame.transform.scale(sprite.image,(TILE_SIDE/2,TILE_SIDE/2))
            SCREEN.blit(image,sprite.rect)
            text = FONT_TURN.render(TEXT_TREASURE,True,YELLOW)  # True means to use anti-aliasing; (255, 255, 255) is the color
            text_rect = text.get_rect()
            text_rect.centerx = GOAL_TEXT_X_CENTER
            text_rect.centery = GOAL_TEXT_Y_CENTER
            SCREEN.blit(text, text_rect)            

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
    text = FONT_TURN.render(TEXT_TURN[Human_Turn], True, COLORS[Human_Turn])  # True means to use anti-aliasing; (255, 255, 255) is the color
    text_rect = text.get_rect()
    text_rect.centerx = TEXT_X_CENTER
    text_rect.centery = TEXT_Y_CENTER
    SCREEN.blit(text, text_rect)

def blitInstructions(instruction):
    text = FONT_INSTRUCTIONS.render(TEXT_INSTRUCTIONS[instruction],True,GRAY)
    text_rect = text.get_rect()
    text_rect.centerx = INSTRUCT_X_CENTER
    text_rect.centery = INSTRUCT_Y_CENTER
    SCREEN.blit(text, text_rect)



Displayed_State = None
def display_state(state:State):
    global WaitingMove
    global WaitingShift

    SCREEN.fill(BLUE)

    # Blit Board
    global BOARD_SPRITES
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
    if WaitingShift:
        blitInstructions(0)
    elif WaitingMove:
        blitInstructions(1)

    pygame.display.update()


def display_state_sequence(states:list[State]):
    display_state(states[0])
    AUDIO_DICT['TileShift'].play()
    pygame.event.pump()
    time.sleep(1.5)
    for s in states[1:]:
        pygame.event.pump()
        display_state(s)
        AUDIO_DICT['PlayerMove'].play()
        time.sleep(0.5)

def handle_rot_click(event):
    global side_tile_rot
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        if ROT_SPRITES[1][0].rect.collidepoint(mouse_pos):
            Displayed_State.side_tile = Displayed_State.side_tile.rotate(-1)
        elif ROT_SPRITES[1][1].rect.collidepoint(mouse_pos):
            Displayed_State.side_tile = Displayed_State.side_tile.rotate(1)
    display_state(Displayed_State)

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
                    states = list(bfs_search_no_goal(Displayed_State,False))
                    for s in states:
                        if s.Human_Pos == [i,j]:
                            return [i,j]
        return None

def handle_again_click(event):
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        if AGAIN_SPRITE.rect.collidepoint(mouse_pos):
            return True
    return False


def human_turn(state:State):
    global Human_Turn
    global WaitingShift
    global WaitingMove
    Human_Turn=True
    AUDIO_DICT['HumanTurn'].play()
    display_state(state)
    WaitingShift=True
    tile_shift=None
    while tile_shift is None:
        for event in pygame.event.get():
            handle_rot_click(event)
            handle_arrow_click(event)
            handle_exit(event)
            tile_shift = handle_arrow_click(event)
    WaitingShift=False
    WaitingMove=True
    state = results(state,tile_shift)
    AUDIO_DICT['TileShift'].play()
    display_state(state)
    blitInstructions(1)
    pygame.display.update()
    tile_clicked = None
    possible_states=list(bfs_search_no_goal(Displayed_State,False))
    if len(possible_states)==1:
        state=possible_states[0]
    else:
        while tile_clicked is None:
            for event in pygame.event.get():
                tile_clicked = handle_tile_click(event)
                handle_exit(event)
        for p in state.players:
            if not p.isAI:
                p.row,p.col = tile_clicked[0],tile_clicked[1]
        AUDIO_DICT['PlayerMove'].play()
        state = State(state.players,state.treasures,state.board,state.side_tile,state.forbidden_shift)
    WaitingMove=False
    Human_Turn = False
    display_state(state)
    return state

def game_ended():
    SCREEN.blit(AGAIN_SPRITE.image,AGAIN_SPRITE.rect)
    pygame.display.update()
    again = False
    while not again:
        for event in pygame.event.get():
            handle_exit(event)
            again = handle_again_click(event)
    

def handle_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()       

def main():
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




    # Update the display
    pygame.display.update()
    
    global Human_Turn
    blitRot(True)
    Human_Turn = False
    display_state(test_state)
    time.sleep(1)
    display_state_sequence(Solution[0])
    blitRot(Human_Turn)
    pygame.display.update()
    Human_Turn=True
    while True:
        human_turn(Displayed_State)
        pygame.display.update()

if __name__=="__main__":
    print('YOU ARE NOT SUPPOSED TO RUN THIS FILE AS SCRIPT')
    main()