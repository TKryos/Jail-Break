import pygame
import sys
from game_parameters import *


#only the overall background
def draw_background(back):
    stairs = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0037.png").convert()
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    for x in range(0,SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            back.blit(stairs, (x,y))

#    for x in range(int(JAIL_X_START), int(JAIL_X_END), int(TILE_SIZE)):
#        for y in range(int(JAIL_Y_START), int(JAIL_Y_END), int(TILE_SIZE)):
#            back.blit(floor, (x,y))

