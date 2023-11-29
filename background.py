import pygame
from game_parameters import *
from tiles_etc import *

#only the overall background
def draw_background(surface):
    surface.fill((84, 84, 84))

    # create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):  # create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            surface.blit(floor.convert(), (x, y))
    for x in range(JAIL_X_START - TILE_SIZE, JAIL_X_END + TILE_SIZE, TILE_SIZE):  # create the top wall
        surface.blit(basic_wall.convert(), (x, JAIL_Y_START - TILE_SIZE))
    for x in range(JAIL_X_START - TILE_SIZE, JAIL_X_END + TILE_SIZE, TILE_SIZE):  # create the bottom wall
        surface.blit(basic_wall.convert(), (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):  # create the left wall
        surface.blit(basic_wall.convert(), (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):  # create the right wall
        surface.blit(basic_wall.convert(), (JAIL_X_END, y))
