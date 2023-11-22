import pygame
from game_parameters import *
from rooms import *
from background import draw_background
from player import Player
from enemy import Guard, enemies, Broken_Prisoner
from objects import Door, doors, Barrier, barriers, Hole, holes

import sys

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#clock object
clock = pygame.time.Clock()

#Main Loop
running = True
background =screen.copy()
#draw_background(background)
background.fill((84, 84, 84))
draw_room2(background)

#create the player
player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

#create the guard
guard = Broken_Prisoner(JAIL_X_START - TILE_SIZE*2*1, JAIL_Y_START - TILE_SIZE*2*1)

#Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #draw background
    screen.blit(background, (0,0))

    #update player location
    player.update(barriers)
    guard.update()
    #draw game objects
    player.draw(screen)
    doors.draw(screen)
    guard.draw(screen)
    #update the display
    pygame.display.flip()

    #limit the fps
    clock.tick(60)

#quit pygame
pygame.quit()