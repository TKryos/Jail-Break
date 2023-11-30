import pygame
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_open_doors, draw_closed_doors,
                   draw_room1, draw_room2, draw_room3, draw_room4, draw_room5,
                   room_choice, r1_e1, r1_e2, r1_e3, r1_e4, )
from player import knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash,
                     door_bot, door_top, door_left, door_right, top_doors, left_doors, right_doors, bot_doors)
from background import draw_background
import random


def room_u(player):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_1")

    draw_background(floor1)

    clock = pygame.time.Clock()



    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((255, 255, 255))

    LAST_THROW_TIME = 0
    LAST_DMG_TIME = 0

    running = True
    while running and player.hp > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
