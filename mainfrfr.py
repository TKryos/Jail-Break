import pygame
import sys
from game_parameters import *
from background import draw_background
from rooms import draw_F1_start_room, draw_open_doors
import tiles_etc
from player import Player

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()

#overall background
draw_background(background)
draw_F1_start_room(background)
draw_open_doors(background)

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

#clock object
clock = pygame.time.Clock()

#make two boxes on the left and right of the screen to start or quit game
Play = tiles_etc.title_font.render("Jail-Break!", True, (150, 150, 150))
Exit = tiles_etc.title_font.render("Exit Game", True, (150, 150, 150))
background.blit(Play, (50, SCREEN_HEIGHT//2 - Play.get_height()//2))
background.blit(Exit, (SCREEN_WIDTH - int(Exit.get_width()) - 50, SCREEN_HEIGHT//2 - Play.get_height()//2))

