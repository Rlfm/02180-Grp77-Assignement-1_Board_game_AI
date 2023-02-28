import pygame
from LabyrinthClasses import Tile
import random
import copy

# Initialize Pygame
pygame.init()

# Set the size of the game screen
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the size of each tile
tile_width = 100
tile_height = 100

arrow_width =15
arrow_height=30

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

arrow = pygame.image.load('sprites/Treasure3.png').convert_alpha()

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
            tiles_sprites[Tile(1,0,1,0).rotate(i)] =sprite
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




screen.fill((47, 60, 113)) #Background color

all_sprites = pygame.sprite.Group()

# Create sprite instances for each tile in the grid and add them to the sprite dictionnary
for row in range(5):
    for col in range(5):
        sprite = tiles_sprites[CurrentTiles[row][col]]
        print((col*20, row*20))
        sprite.rect.topleft = (50+col*100, 50+row*100)
        screen.blit(sprite.image, sprite.rect)


# Update the display
pygame.display.update()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()