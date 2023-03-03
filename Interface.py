import pygame
from States import *
import random
import copy

# Initialize Pygame
pygame.init()

MARGIN = 50
DASHBOARD = 200
TILE_SIDE = 100
ROWS = 5
COLS = 5

# Set the size of the game SCREEN
SCREEN_WIDTH = TILE_SIDE*COLS+2*MARGIN+DASHBOARD
SCREEN_HEIGHT = TILE_SIDE*ROWS+2*MARGIN
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SIDE_TILE_X = MARGIN*2+TILE_SIDE*COLS+DASHBOARD/2
SIDE_TILE_Y = TILE_SIDE

# Set the size of each tile
tile_width = TILE_SIDE
tile_height = TILE_SIDE

arrow_height = TILE_SIDE/3
arrow_width = arrow_height/2

rot_width = TILE_SIDE/2
rot_height = rot_width/2

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
        if treasure.x == None:
            sprite.rect.center = (SIDE_TILE_X,SIDE_TILE_Y)
        else: 
            sprite.rect.center = (MARGIN+TILE_SIDE*(treasure.x+0.5),MARGIN+TILE_SIDE*(treasure.y+0.5))
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

        sprite.rect.center = (MARGIN+TILE_SIDE*(player.x+0.5),MARGIN+TILE_SIDE*(player.y+0.5))

    if PLAYER_SPRITES[0].rect.center == PLAYER_SPRITES[1].rect.center:
        PLAYER_SPRITES[0].rect.x = PLAYER_SPRITES[0].rect.x-TILE_SIDE/7
        PLAYER_SPRITES[1].rect.x = PLAYER_SPRITES[1].rect.x+TILE_SIDE/7
    SCREEN.blit(PLAYER_SPRITES[0].image,PLAYER_SPRITES[0].rect)
    SCREEN.blit(PLAYER_SPRITES[1].image,PLAYER_SPRITES[1].rect)


# Load shifting arrows sprites
ARR0W_IMAGES = [pygame.transform.scale(pygame.image.load('sprites/arrow_unavailable.png').convert_alpha(),(arrow_width,arrow_height)),
                pygame.transform.scale(pygame.image.load('sprites/arrow.png').convert_alpha(),(arrow_width,arrow_height))]
odds = [num for num in range(ROWS) if num % 2 != 0]
ARROW_SPRITES = [[[pygame.sprite.Sprite() for _ in range(4)] for _ in range(len(odds))] for _ in range(2)]
for i in range(4):
    for j in range(len(odds)):
        for k in range(2):
            rotated_image = pygame.transform.rotate(ARR0W_IMAGES[k], i*-90)

            sprite = pygame.sprite.Sprite()
            sprite.image = rotated_image
            sprite.rect = rotated_image.get_rect()

            if i%2==0:
                sprite.rect.center = (MARGIN*(i+1)/2+(i/2)*COLS*TILE_SIDE, MARGIN+(j*2+1+.5)*TILE_SIDE)
            else:
                sprite.rect.center = (MARGIN+(j*2+1+.5)*TILE_SIDE, MARGIN*(i)/2+((i-1)/2)*ROWS*TILE_SIDE)
            ARROW_SPRITES[k][j][i] = sprite

SCREEN.fill((47, 60, 113)) #Background color

# Display the arrows, side after side
def blitArrows(state:State):
    forbidden_shift = state.forbidden_shift
    j=[i for i in range(4)]
    odds = [num for num in range(ROWS) if num % 2 != 0]
    evens = [num for num in range(ROWS) if num % 2 == 0]
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

    for k in range(len(ARROW_SPRITES[0])):
        for m in range(len(ARROW_SPRITES[0][0])):
            sprite = ARROW_SPRITES[not (k==i and m==j)][k][m]
            SCREEN.blit(sprite.image,sprite.rect)
    

# Load rotating arrows sprites
rot_images = [pygame.transform.scale(pygame.image.load('sprites/arrow_rot_unavailable.png').convert_alpha(),(rot_width,rot_height)),
              pygame.transform.scale(pygame.image.load('sprites/arrow_rot.png').convert_alpha(),(rot_width,rot_height))]
rot_sprites={}
for i in range(2):
    sprite = pygame.sprite.Sprite()
    sprite.image = rot_images[i]
    sprite.rect = sprite.image.get_rect()
    rot_sprites[i]=sprite


def fill_board_sprites(board,tile_sprites,tile_images):
    w,h = len(board),len(board[0])
    for i in range(w):
        for j in range(h):
            tile_sprites[i][j].image = tile_images[board[i][j]]
    return tile_sprites


def display_state(state:State):
    # Blit Board
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
    #TODO: finish the function




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

CurrentTiles = [[copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_2),copy.deepcopy(T_3),copy.deepcopy(T_4)],
		[copy.deepcopy(Straight1),copy.deepcopy(T_4),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_2)],
		[copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(T_1),copy.deepcopy(T_3),copy.deepcopy(Straight1)],
		[copy.deepcopy(Corner2),copy.deepcopy(Corner4),copy.deepcopy(Corner1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],
		[copy.deepcopy(Straight2),copy.deepcopy(Corner3),copy.deepcopy(Straight1),copy.deepcopy(Straight1),copy.deepcopy(Straight1)],]



forbidden_shift = TileShiftAction(None,1,1,1)
#(None,1,3,-1)

treasures = generate_treasures(ROWS,2)
treasures.append(Treasure(None,None,2))


AI = Player(0,1,treasures[0],True)
Human = Player(0,0,treasures[1],False)

test_state = State([AI,Human],treasures,CurrentTiles,Tile(0,0,1,1),forbidden_shift)

# Update the display
pygame.display.update()



def main():

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(MARGIN+TILE_SIDE*j,MARGIN+TILE_SIDE*i,TILE_SIDE,TILE_SIDE)
            BOARD_SPRITES[i][j].rect = rect
    

    display_state(test_state)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()

if __name__=="__main__":
    main()