import pygame
from LabyrinthClasses import *
import random
import copy

# Initialize Pygame
pygame.init()

MARGIN = 50
DASHBOARD = 200
TILE_SIDE = 100
ROWS = 5
COLS = 5

# Set the size of the game screen
screen_width = TILE_SIDE*COLS+2*MARGIN+DASHBOARD
screen_height = TILE_SIDE*ROWS+2*MARGIN
screen = pygame.display.set_mode((screen_width, screen_height))

side_tile_x = MARGIN*2+TILE_SIDE*COLS+DASHBOARD/2
side_tile_y = TILE_SIDE

# Set the size of each tile
tile_width = TILE_SIDE
tile_height = TILE_SIDE

arrow_height = TILE_SIDE/3
arrow_width = arrow_height/2

rot_width = TILE_SIDE/2
rot_height = rot_width/2

# Load the sprite images
tiles_images = {
    'corner':pygame.image.load('sprites/Tile_Corner.png').convert_alpha(),
    'straight':pygame.image.load('sprites/Tile_Straight.png').convert_alpha(),
    'T':pygame.image.load('sprites/Tile_T.png').convert_alpha()}


# Create a sprite dictionnary
tiles_sprites ={}

# Create rotated versions of each tile image and add them to the appropriate sprite groups
for tile_name, tile_image in tiles_images.items():

    tile_image = pygame.transform.scale(tile_image,(tile_width,tile_height))
    if tile_name == 'straight':
        # Straight tile has only 2 possible rotations
        for i in range(2):
            rotated_image = pygame.transform.rotate(tile_image, i*-90)
            sprite = pygame.sprite.Sprite()
            sprite.image = rotated_image
            sprite.rect = sprite.image.get_rect()
            tiles_sprites[Tile(1,0,1,0).rotate(i)] = sprite
    else:
        # All other tiles have 4 possible rotations
        for i in range(4):
            rotated_image = pygame.transform.rotate(tile_image, i*-90)
            sprite = pygame.sprite.Sprite()
            sprite.image = rotated_image
            sprite.rect = sprite.image.get_rect()
            if tile_name == 'corner':
                tiles_sprites[Tile(0,1,1,0).rotate(i)] = sprite
            elif tile_name == 'T':
                tiles_sprites[Tile(1,1,1,0).rotate(i)] = sprite

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

def blitTreasure(treasure:Treasure):
    sprite = treasure_sprites[treasure.id]
    if treasure.x == None:
        sprite.rect.center = (side_tile_x,side_tile_y)
    else: 
        sprite.rect.center = (MARGIN+TILE_SIDE*(treasure.x+0.5),MARGIN+TILE_SIDE*(treasure.y+0.5))
    screen.blit(sprite.image,sprite.rect)

# Load player images
player_images = [pygame.image.load('sprites/player1.png').convert_alpha(),
                   pygame.image.load('sprites/player2.png').convert_alpha()]

player_sprites = [0]*len(player_images)

for i in range(len(player_images)):
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(player_images[i],(TILE_SIDE/2.5,TILE_SIDE/2.5))
    sprite.rect = sprite.image.get_rect()
    player_sprites[i] = sprite

def blitPlayer(player:Player):
    if player.isAI: sprite = player_sprites[0]
    else: sprite = player_sprites[1]
    sprite.rect.center = (MARGIN+TILE_SIDE*(player.x+0.5),MARGIN+TILE_SIDE*(player.y+0.5))
    screen.blit(sprite.image,sprite.rect)


# Load shifting arrows sprites
arrow_images = [pygame.transform.scale(pygame.image.load('sprites/arrow_unavailable.png').convert_alpha(),(arrow_width,arrow_height)),
                pygame.transform.scale(pygame.image.load('sprites/arrow.png').convert_alpha(),(arrow_width,arrow_height))]
arrow_sprites=[[0]*4]*2
for i in range(4):
    for j in range(2):
        rotated_image = pygame.transform.rotate(arrow_images[j], i*-90)
        sprite = pygame.sprite.Sprite()
        sprite.image = rotated_image
        sprite.rect = sprite.image.get_rect()
        arrow_sprites[j][i] = sprite

screen.fill((47, 60, 113)) #Background color

# Display the arrows, side after side
#TODO: Add support for forbidden shifts
def blitArrows(screen,forbidden_shift:TileShiftAction):
    for i in range(4):
        odds = [num for num in range(ROWS) if num % 2 != 0]
        for j in odds:
            sprite = arrow_sprites[0][i]
            if i%2==0:
                sprite.rect.center = (MARGIN*(i+1)/2+(i/2)*COLS*TILE_SIDE, MARGIN+(j+.5)*TILE_SIDE)
            else:
                sprite.rect.center = (MARGIN+(j+.5)*TILE_SIDE, MARGIN*(i)/2+((i-1)/2)*ROWS*TILE_SIDE)

            screen.blit(sprite.image, sprite.rect)

# Load rotating arrows sprites
rot_images = [pygame.transform.scale(pygame.image.load('sprites/arrow_rot_unavailable.png').convert_alpha(),(rot_width,rot_height)),
              pygame.transform.scale(pygame.image.load('sprites/arrow_rot.png').convert_alpha(),(rot_width,rot_height))]
rot_sprites={}
for i in range(2):
    sprite = pygame.sprite.Sprite()
    sprite.image = rot_images[i]
    sprite.rect = sprite.image.get_rect()
    rot_sprites[i]=sprite

def blitBoard(board, screen):
    #Draws a board on the screen
    rows = len(board)
    cols = len(board[0])
    # Create sprite instances for each tile in the grid and add them to the sprite dictionnary
    for row in range(rows):
        for col in range(cols):
            sprite = tiles_sprites[board[row][col]]
            sprite.rect.topleft = (50+col*100, 50+row*100)
            screen.blit(sprite.image, sprite.rect)

def blitSideTile(tile,screen):
    sprite = tiles_sprites[tile]
    sprite.rect.center = (side_tile_x,side_tile_y)
    screen.blit(sprite.image,sprite.rect)


def animateTileShift(board,tileShiftAction):
    #TODO: Write the tile shift animation
    pass


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



forbidden_shift = TileShiftAction(None,1,3,1)
blitArrows(screen,forbidden_shift)
blitBoard(CurrentTiles,screen)
blitSideTile(Tile(0,1,1,0),screen)
treasures = generate_treasures(ROWS,2)
treasures.append(Treasure(None,None,2))
for treasure in treasures:
    blitTreasure(treasure)

AI = Player(0,0,treasures[0],True)
Human = Player(4,4,treasures[1],False)
blitPlayer(AI)
blitPlayer(Human)

# Update the display
pygame.display.update()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()