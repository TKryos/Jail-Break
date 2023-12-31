import pygame
import sys

from game_parameters import *
from rooms import draw_f1_start_room
from door_layouts import draw_open_doors
from background import draw_background
from tiles_etc import title_font
from player import Player
from objects import clear_objects
import floor_one, floor_two, floor_three, floor_four, floor_five


#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()
pygame.display.set_caption("JailBreak: Title Screen")

#overall background
draw_background(background)
draw_f1_start_room(background)
draw_open_doors(background)

floor_states = {'floor 1': 0, 'floor 2': 0, 'floor 3': 0, 'floor 4': 0, 'floor 5': 0}

#create the player
thief = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
background.blit(thief.image, (SCREEN_WIDTH//2 - 14, SCREEN_HEIGHT//2 - 14))

LIVES = thief.hp
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

TIME = 0
LAST_THROW_TIME = 0
LAST_DMG_TIME = 0
TIME_SINCE_DOOR = 0
TIME_LAST_SCORE = 0
#Main Loop
game = True

while game and thief.hp > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse clicked on the playbutton
                if play_button_rect.collidepoint(mouse_pos):
                    if sum(floor_states.values()) == 0:

                        clear_objects()
                        floor_one.main(thief, floor_states)
                    if sum(floor_states.values()) == 1:

                        clear_objects()
                        floor_two.main(thief, floor_states)

                    if sum(floor_states.values()) == 2:

                        clear_objects()
                        floor_three.main(thief, floor_states)

                    if sum(floor_states.values()) == 3:

                        clear_objects()
                        floor_four.main(thief, floor_states)

                    if sum(floor_states.values()) == 4:

                        clear_objects()
                        floor_five.main(thief, floor_states)

                    if sum(floor_states.values()) == 5:
                        game = False

                # Check if the mouse clicked on the exit button
                elif exit_button_rect.collidepoint(mouse_pos):
                    game = False

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the buttons
    pygame.draw.rect(screen, (0, 200, 0), play_button_rect)
    pygame.draw.rect(screen, (200, 0, 0), exit_button_rect)

    for i in range(thief.hp):
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


#create the screen
screen.blit(background, (0,0))
pygame.display.set_caption("JailBreak: End Screen")

#make two boxes on the left and right of the screen to start or quit game
if sum(floor_states.values()) < 5:
    End_text = title_font.render(f"You got through {sum(floor_states.values())} floors.", True, (0, 0, 0))
    screen.blit(End_text, (SCREEN_WIDTH//2 - End_text.get_width()//2, SCREEN_HEIGHT//2 - End_text.get_height()*5))

elif sum(floor_states.values()) == 5:
    End_text = title_font.render("You escaped the jail!", True, (0, 0, 0))
    screen.blit(End_text, (SCREEN_WIDTH//2 - End_text.get_width()//2, SCREEN_HEIGHT//2 - End_text.get_height()*5))



pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()