import pygame
from game_parameters import *
from objects import *
from background import *
from tiles_etc import *




#the different possible rooms that can be drawn

#starting floor for each floor/level
def draw_F1_start_room(room):
    """basic room with simple instruction on how to play"""
    tutorial_1 = tutorial_font.render("Use WASD to move", True, (150, 150, 150))
    tutorial_2 = tutorial_font.render("Point and click to throw knives", True, (150, 150, 150))
    tutorial_3 = tutorial_font.render("Defeat guards,get items, ESCAPE", True, (150, 150, 150))
    room.blit(tutorial_1, (SCREEN_WIDTH//2 - tutorial_1.get_width()/2, JAIL_Y_START))
    room.blit(tutorial_2, (SCREEN_WIDTH//2 - tutorial_2.get_width()/2, SCREEN_HEIGHT//2))
    room.blit(tutorial_3, (SCREEN_WIDTH//2 - tutorial_3.get_width()/2, JAIL_Y_END - tutorial_3.get_height()))

def draw_closed_doors(room):
    #doors.add(door_top, door_left, door_right, door_bot)
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE))
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE*3))
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE*3))

def draw_open_doors(room):
    doors.add(door_top, door_left, door_right, door_bot)
    room.blit(door_open.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))
    room.blit(pygame.transform.rotate(door_open.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_open.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(door_open.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))
def draw_room1(room):
####create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*3, JAIL_Y_START + TILE_SIZE*2, TILE_SIZE*7, TILE_SIZE*3))
    for x in range(JAIL_X_START + TILE_SIZE*3, JAIL_X_END - TILE_SIZE*3, TILE_SIZE):
        for y in range(JAIL_Y_START + TILE_SIZE*2, JAIL_Y_END - TILE_SIZE*2, TILE_SIZE):
            room.blit(basic_wall, (x, y))
    #create the doors
    #room.blit(door_open, ())

def draw_room2(room):
####create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*3, JAIL_Y_START + TILE_SIZE*1, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*3, JAIL_Y_START + TILE_SIZE))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*9, JAIL_Y_START + TILE_SIZE*1, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*9, JAIL_Y_START + TILE_SIZE))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*3, JAIL_Y_START + TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*3, JAIL_Y_START + TILE_SIZE*5))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*9, JAIL_Y_START + TILE_SIZE*5, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*9, JAIL_Y_START + TILE_SIZE*5))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*1, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE*3))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*3))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*11, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*11, JAIL_Y_START + TILE_SIZE*3))

def draw_room3(room):
####create the specific obstacles
####top left corner
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_START, TILE_SIZE*4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*x, JAIL_Y_START))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START, JAIL_Y_START + TILE_SIZE))
####top right corner
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*9, JAIL_Y_START, TILE_SIZE*4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*(x+9), JAIL_Y_START))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE))
####bot left corner
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE, TILE_SIZE*4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*x, JAIL_Y_END - TILE_SIZE))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE*2, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START, JAIL_Y_END - TILE_SIZE*2))
####bot right corner
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE*9, JAIL_Y_END - TILE_SIZE, TILE_SIZE*4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE*(9+x), JAIL_Y_END - TILE_SIZE))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE*2, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE*2))

def draw_room4(room):
    floor_gash.set_colorkey((255, 255, 255))
    #create the specific obstacles
####top left
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE, JAIL_Y_START, TILE_SIZE*2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*(1+x), JAIL_Y_START))
    floor_gashes.add(Floor_Gash(JAIL_X_START, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START, JAIL_Y_START + TILE_SIZE))
####top right
    floor_gashes.add(Floor_Gash(JAIL_X_END - TILE_SIZE*3, JAIL_Y_START, TILE_SIZE*2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE*(2+x), JAIL_Y_START))
    floor_gashes.add(Floor_Gash(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE))
####bottom left
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, TILE_SIZE*2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*(1+x), JAIL_Y_END - TILE_SIZE))
    floor_gashes.add(Floor_Gash(JAIL_X_START, JAIL_Y_END - TILE_SIZE*2, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START, JAIL_Y_END - TILE_SIZE*2))
####bottom right
    floor_gashes.add(Floor_Gash(JAIL_X_END - TILE_SIZE*3, JAIL_Y_END - TILE_SIZE, TILE_SIZE*2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE*(2+x), JAIL_Y_END - TILE_SIZE))
    floor_gashes.add(Floor_Gash(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE*2, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE*2))

def draw_room5(room):
    floor_gash.set_colorkey((255, 255, 255))

####middle island
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE*5, JAIL_Y_START + TILE_SIZE*2, TILE_SIZE*3, TILE_SIZE))
    for x in range(3):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*(5+x), JAIL_Y_START + TILE_SIZE*2))
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE*5, JAIL_Y_START + TILE_SIZE*4, TILE_SIZE*3, TILE_SIZE))
    for x in range(3):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*(5+x), JAIL_Y_START + TILE_SIZE*4))
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3))
    floor_gashes.add(Floor_Gash(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3))

#def draw_room6(room):

#def draw_boss_room1(room):

#def draw_boss_room2(room):

#def draw_final_boss(room):
