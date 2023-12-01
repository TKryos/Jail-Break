import pygame
import sys

from game_parameters import *
from rooms import draw_f1_start_room
from door_layouts import draw_open_doors
from background import draw_background
from tiles_etc import title_font
from player import Player
import floor_one


#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()

#overall background
draw_background(background)
draw_f1_start_room(background)
draw_open_doors(background)

#create the player
theif = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
background.blit(theif.image, (SCREEN_WIDTH//2 - 14, SCREEN_HEIGHT//2 - 14))

LIVES = theif.hp
hearts = pygame.image.load("assets/tiles/heart.png").convert()
hearts.set_colorkey((0, 0, 0))
#clock object
clock = pygame.time.Clock()

#make two boxes on the left and right of the screen to start or quit game
Play = title_font.render("Jail-Break!", True, (0, 0, 0))
Exit = title_font.render("Exit Game", True, (0, 0, 0))
background.blit(Play, (50, SCREEN_HEIGHT//2 - Play.get_height()//2))
background.blit(Exit, (SCREEN_WIDTH - int(Exit.get_width()) - 50, SCREEN_HEIGHT//2 - Play.get_height()//2))
play_button_rect = pygame.Rect(40, SCREEN_HEIGHT//2 - 35, 280, 65)
exit_button_rect = pygame.Rect((SCREEN_WIDTH - 305, SCREEN_HEIGHT//2 - 35, 265, 65))

LAST_THROW_TIME = 0
LAST_DMG_TIME = 0
TIME_SINCE_DOOR = 0
#Main Loop
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse clicked on the playbutton
                if play_button_rect.collidepoint(mouse_pos):
                    floor_one.main(theif)


                # Check if the mouse clicked on the exit button
                elif exit_button_rect.collidepoint(mouse_pos):
                    game = False

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the buttons
    pygame.draw.rect(screen, (0, 200, 0), play_button_rect)
    pygame.draw.rect(screen, (200, 0, 0), exit_button_rect)

    for i in range(theif.hp):
        if i <= 9:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-1), JAIL_Y_END + TILE_SIZE))
        elif i <= 19:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-11), JAIL_Y_END + TILE_SIZE*2))
        elif i <= 29:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-21), JAIL_Y_END + TILE_SIZE*3))

    # Draw the text over the button rectangles
    Play = title_font.render("Jail-Break!", True, (0, 0, 0))
    Exit = title_font.render("Exit Game", True, (0, 0, 0))
    screen.blit(Play, (50, SCREEN_HEIGHT // 2 - Play.get_height() // 2))
    screen.blit(Exit, (SCREEN_WIDTH - int(Exit.get_width()) - 50, SCREEN_HEIGHT // 2 - Play.get_height() // 2))

    #update the display
    pygame.display.flip()

    #limit the fps
    clock.tick(30)

#quit pygame
pygame.quit()
sys.exit()