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

stair_image = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0039.png"),
    (32, 32))

health_pot = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0115.png"),
    (32, 32))
maxhpup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0124.png"),
    (32, 32))
atkup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0074.png"),
    (32, 32))
atkrngup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0116.png"),
    (32, 32))
atkspdup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0113.png"),
    (32, 32))
knifespdup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0125.png"),
    (32, 32))
spdup = pygame.transform.scale(
    pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0114.png"),
    (32, 32))
