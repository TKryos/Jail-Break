import pygame
from game_parameters import *
from background import draw_background
from player import Player

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#clock object
clock = pygame.time.Clock()

#setup
running = True
background =screen.copy()
draw_background(background)

#create the player
player = Player(JAIL_X_START + TILE_SIZE, SCREEN_HEIGHT/2)

# the different possible floors that can be drawn

def draw_start_room(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

    # create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):  # create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START - TILE_SIZE, JAIL_X_END + TILE_SIZE, TILE_SIZE):  # create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START - TILE_SIZE))
    for x in range(JAIL_X_START - TILE_SIZE, JAIL_X_END + TILE_SIZE, TILE_SIZE):  # create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):  # create the left wall
        room.blit(basic_wall, (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):  # create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))


    for x in range(JAIL_X_START + TILE_SIZE*3*2, JAIL_X_END - TILE_SIZE*(3*2+1), TILE_SIZE):
        for y in range(JAIL_Y_START + TILE_SIZE*2*2, JAIL_Y_END - TILE_SIZE*(2*2+1), TILE_SIZE):
            barrier = Barrier(x, y, TILE_SIZE, TILE_SIZE)
            barriers.add(barrier)
            room.blit(basic_wall, (x, y))


draw_start_room(background)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    barriers.draw(screen)

    # draw background
    screen.blit(background, (0, 0))

    #update barriers
    barriers.update()

    # update player location
    player.update(barriers)

    # draw game objects
    player.draw(screen)


    # update the display
    pygame.display.flip()

    #limit the fps
    clock.tick(60)

# quit pygame
pygame.quit()