import pygame
pygame.init()


title_font = pygame.font.Font("assets/fonts/Black_Crayon.ttf", 50)
tutorial_font = pygame.font.Font("assets/fonts/Black_Crayon.ttf", 20)


floor = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png"),
    (32, 32))
basic_wall = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png"),
    (32, 32))
door_closed = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0045.png"),
    (32, 32))
door_open = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0009.png"),
    (32, 32))
floor_gash = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0062.png"),
    (32, 32))
boss_door_indicators = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0019.png"),
    (32, 32))
item_door_indicators = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0029.png"),
    (32, 32))