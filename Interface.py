import pygame
from LabyrinthClasses import Tile
import random
import copy

# Initialize Pygame
pygame.init()

MARGIN = 50
TILE_SIDE = 100
ROWS = 5
COLS = 5

# Set the size of the game screen
screen_width = TILE_SIDE*COLS+2*MARGIN
screen_height = TILE_SIDE*ROWS+2*MARGIN
screen = pygame.display.set_mode((screen_width, screen_height))


# Set the size of each tile
tile_width = TILE_SIDE
tile_height = TILE_SIDE

arrow_height = TILE_SIDE/3
arrow_width = arrow_height/2

# Load the sprite images
tiles_images = {
    'corner':pygame.image.load('sprites/Tile_Corner.png').convert_alpha(),
    'straight':pygame.image.load('sprites/Tile_Straight.png').convert_alpha(),
    'T':pygame.image.load('sprites/Tile_T.png').convert_alpha(),
    'treasure0':pygame.image.load('sprites/Treasure0.png').convert_alpha(),
    'treasure1':pygame.image.load('sprites/Treasure1.png').convert_alpha(),
    'treasure2':pygame.image.load('sprites/Treasure2.png').convert_alpha(),
    'treasure3':pygame.image.load('sprites/Treasure3.png').convert_alpha()
}


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
            #TODO: Add different types of treasure tiles (for now: only straight North/South)
            else:
                pass
                #tiles_sprites[Tile(1,0,1,0).rotate(i)] = sprite

# Load the other sprites
arrow_image = pygame.transform.scale(pygame.image.load('sprites/arrow.png').convert_alpha(),(arrow_width,arrow_height))
arrow_sprites=[0]*4
for i in range(4):
    rotated_image = pygame.transform.rotate(arrow_image, i*-90)
    sprite = pygame.sprite.Sprite()
    sprite.image = rotated_image
    sprite.rect = sprite.image.get_rect()
    arrow_sprites[i] = sprite


screen.fill((47, 60, 113)) #Background color

# Display the arrows, side after side
for i in range(4):
    odds = [num for num in range(ROWS) if num % 2 != 0]
    for j in odds:
        sprite = arrow_sprites[i]
        if i%2==0:
            sprite.rect.center = (MARGIN*(i+1)/2+(i/2)*COLS*TILE_SIDE, MARGIN+(j+.5)*TILE_SIDE)
            print(sprite.rect.center)
        else:
            sprite.rect.center = (MARGIN+(j+.5)*TILE_SIDE, MARGIN*(i)/2+((i-1)/2)*ROWS*TILE_SIDE)
            print(sprite.rect.center)

        screen.blit(sprite.image, sprite.rect)

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





blitBoard(CurrentTiles,screen)

# Update the display
pygame.display.update()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()