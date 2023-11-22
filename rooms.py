import pygame
from game_parameters import *
from objects import Barrier, barriers, Door, doors, Hole, holes
from tiles import *
#the different possible rooms that can be drawn

#starting floor for each floor/level
def draw_start_room(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

#    #create one barrier for the collision to work out
#    barrier = Barrier(0, 0, TILE_SIZE, TILE_SIZE)
#    barriers.add(barrier)

    #create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):        #create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START-TILE_SIZE))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the left wall
        room.blit(basic_wall, (JAIL_X_START-TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))

def draw_room1(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()
    door_closed = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0047.png").convert()
    door_open = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0011.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

    #create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):        #create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START-TILE_SIZE))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the left wall
        room.blit(basic_wall, (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))

    #create the specific obstacles
    for x in range(JAIL_X_START + TILE_SIZE*3*2, JAIL_X_END - TILE_SIZE*3*2, TILE_SIZE):
        for y in range(JAIL_Y_START + TILE_SIZE*2*2, JAIL_Y_END - TILE_SIZE*2*2, TILE_SIZE):
            barrier = Barrier(x, y, TILE_SIZE, TILE_SIZE)
            barriers.add(barrier)
            room.blit(basic_wall, (x, y))
    #create the doors
    #room.blit(door_open, ())

def draw_room2(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()
    door_closed = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0047.png").convert()
    door_open = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0011.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

    #create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):        #create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START-TILE_SIZE))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the left wall
        room.blit(basic_wall, (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))

    #create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*3, JAIL_Y_START + TILE_SIZE*2*1, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*3+x), JAIL_Y_START + TILE_SIZE*(2*1+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*9, JAIL_Y_START + TILE_SIZE*2*1, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*9+x), JAIL_Y_START + TILE_SIZE*(2*1+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*3, JAIL_Y_START + TILE_SIZE*2*5, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*3+x), JAIL_Y_START + TILE_SIZE*(2*5+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*9, JAIL_Y_START + TILE_SIZE*2*5, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*9+x), JAIL_Y_START + TILE_SIZE*(2*5+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*1, JAIL_Y_START + TILE_SIZE*2*3, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*1+x), JAIL_Y_START + TILE_SIZE*(2*3+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*6, JAIL_Y_START + TILE_SIZE*2*3, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*6+x), JAIL_Y_START + TILE_SIZE*(2*3+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*11, JAIL_Y_START + TILE_SIZE*2*3, TILE_SIZE*2, TILE_SIZE*2))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*11+x), JAIL_Y_START + TILE_SIZE*(2*3+y)))

def draw_room3(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()
    door_closed = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0047.png").convert()
    door_open = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0011.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

    #create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):        #create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START-TILE_SIZE))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the left wall
        room.blit(basic_wall, (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))

    #create the specific obstacles
    #top left corner
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*(2*1), JAIL_Y_START, TILE_SIZE*2*3, TILE_SIZE*2*1))
    for x in range(0,8):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*0+x), JAIL_Y_START + TILE_SIZE*(2*0+y)))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_START + TILE_SIZE*2*1, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*0+x), JAIL_Y_START + TILE_SIZE*(2*1+y)))
    #top right corner
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE*(2*4), JAIL_Y_START, TILE_SIZE*2*4, TILE_SIZE*2*1))
    for x in range(0,8):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_END - TILE_SIZE*(2*4-x), JAIL_Y_START + TILE_SIZE*(2*0+y)))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE*2*1, JAIL_Y_START + TILE_SIZE*2*1, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_END - TILE_SIZE*(2*1-x), JAIL_Y_START + TILE_SIZE*(2*1+y)))
    #bot left corner
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE*2*1, TILE_SIZE*2*4, TILE_SIZE*2*1))
    for x in range(0,8):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*0+x), JAIL_Y_END - TILE_SIZE*(2*1-1+y)))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE*2*2, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*0+x), JAIL_Y_END - TILE_SIZE*(2*2-1+y)))
    #bot right corner
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE*(2*4), JAIL_Y_END - TILE_SIZE*(2*1), TILE_SIZE*2*4, TILE_SIZE*2*1))
    for x in range(0,8):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_END - TILE_SIZE*(2*4-x), JAIL_Y_END - TILE_SIZE*(2*0+1+y)))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE*2*1, JAIL_Y_END - TILE_SIZE*2*2, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_END - TILE_SIZE*(2*1-x), JAIL_Y_END - TILE_SIZE*(2*2-y)))

def draw_room4(room):
    floor = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0000.png").convert()
    basic_wall = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0014.png").convert()
    door_closed = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0047.png").convert()
    door_open = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0011.png").convert()

    floor.set_colorkey((0, 0, 0))
    basic_wall.set_colorkey((0, 0, 0))

    #create the basic shape of each jail room
    for x in range(JAIL_X_START, JAIL_X_END, TILE_SIZE):        #create the floor of the jail
        for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):
            room.blit(floor, (x, y))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the top wall
        room.blit(basic_wall, (x, JAIL_Y_START-TILE_SIZE))
    for x in range(JAIL_X_START-TILE_SIZE, JAIL_X_END+TILE_SIZE, TILE_SIZE):        #create the bottom wall
        room.blit(basic_wall, (x, JAIL_Y_END))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the left wall
        room.blit(basic_wall, (JAIL_X_START - TILE_SIZE, y))
    for y in range(JAIL_Y_START, JAIL_Y_END, TILE_SIZE):        #create the right wall
        room.blit(basic_wall, (JAIL_X_END, y))

    #create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*2, JAIL_Y_START + TILE_SIZE*2*2, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*2+x), JAIL_Y_START + TILE_SIZE*(2*2+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*3, JAIL_Y_START + TILE_SIZE*2*1, TILE_SIZE*2*7, TILE_SIZE*2*1))
    for x in range(0,14):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*3+x), JAIL_Y_START + TILE_SIZE*(2*1+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*10, JAIL_Y_START + TILE_SIZE*2*2, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*10+x), JAIL_Y_START + TILE_SIZE*(2*2+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*2, JAIL_Y_START + TILE_SIZE*2*4, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*2+x), JAIL_Y_START + TILE_SIZE*(2*4+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*3, JAIL_Y_START + TILE_SIZE*2*5, TILE_SIZE*2*7, TILE_SIZE*2*1))
    for x in range(0,14):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*3+x), JAIL_Y_START + TILE_SIZE*(2*5+y)))
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*2*10, JAIL_Y_START + TILE_SIZE*2*4, TILE_SIZE*2*1, TILE_SIZE*2*1))
    for x in range(0,2):
        for y in range(0,2):
            room.blit(basic_wall, (JAIL_X_START + TILE_SIZE*(2*10+x), JAIL_Y_START + TILE_SIZE*(2*4+y)))
#def draw_room5(room):

#def draw_room6(room):

#def draw_boss_room1(room):

#def draw_boss_room2(room):

#def draw_final_boss(room):
