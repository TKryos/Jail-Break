import pygame
from game_parameters import *
from objects import (top_doors, bot_doors, left_doors, right_doors, door_top, door_left, door_right, door_bot,
                     barriers, Barrier, floor_gashes, FloorGash)
from tiles_etc import tutorial_font, door_open, door_closed, basic_wall, floor_gash
from enemy import (patrols, Patrol, sentries, Sentry,
                   guards, Guard, broken_prisoners, Broken_Prisoner)

# the different possible rooms that can be drawn

# starting floor for each floor/level


def draw_f1_start_room(room):
    """basic room with simple instruction on how to play"""
    tutorial_1 = tutorial_font.render("Use WASD to move", True, (150, 150, 150))
    tutorial_2 = tutorial_font.render("Point and click to throw knives", True, (150, 150, 150))
    tutorial_3 = tutorial_font.render("Defeat guards,get items, ESCAPE", True, (150, 150, 150))
    room.blit(tutorial_1, (SCREEN_WIDTH // 2 - tutorial_1.get_width() / 2, JAIL_Y_START))
    room.blit(tutorial_2, (SCREEN_WIDTH // 2 - tutorial_2.get_width() / 2, SCREEN_HEIGHT // 2))
    room.blit(tutorial_3, (SCREEN_WIDTH // 2 - tutorial_3.get_width() / 2, JAIL_Y_END - tutorial_3.get_height()))


def draw_start_room(room):
    """basic room with simple instruction on how to play"""
    tutorial_1 = tutorial_font.render("Use WASD to move", True, (150, 150, 150))
    tutorial_2 = tutorial_font.render("Point and click to throw knives", True, (150, 150, 150))
    tutorial_3 = tutorial_font.render("Defeat guards,get items, ESCAPE", True, (150, 150, 150))
    room.blit(tutorial_1, (SCREEN_WIDTH // 2 - tutorial_1.get_width() / 2, JAIL_Y_START))
    room.blit(tutorial_2, (SCREEN_WIDTH // 2 - tutorial_2.get_width() / 2, SCREEN_HEIGHT // 2))
    room.blit(tutorial_3, (SCREEN_WIDTH // 2 - tutorial_3.get_width() / 2, JAIL_Y_END - tutorial_3.get_height()))


def draw_closed_doors(room):
    # doors.add(door_top, door_left, door_right, door_bot)
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))


def draw_open_doors(room):
    top_doors.add(door_top)
    bot_doors.add(door_bot)
    left_doors.add(door_left)
    right_doors.add(door_right)
    room.blit(door_open.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))
    room.blit(pygame.transform.rotate(door_open.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_open.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(door_open.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))


def draw_room0(room):
    """Just an empty room"""
    pass


def draw_room1(room):
    # Create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 2, TILE_SIZE * 7, TILE_SIZE * 3))
    for x in range(JAIL_X_START + TILE_SIZE * 3, JAIL_X_END - TILE_SIZE * 3, TILE_SIZE):
        for y in range(JAIL_Y_START + TILE_SIZE * 2, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE):
            room.blit(basic_wall, (x, y))


# The parenthesis can house the enemy stats if wanted
def r1_e1():
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE))


def r1_e2():
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE))


def r1_e3():
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE))


def r1_e4(player):
    guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, player))


def draw_room2(room):
    # Create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 1, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 1, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 5, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 5))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 5, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 5))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 1, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))

    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 11, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * 11, JAIL_Y_START + TILE_SIZE * 3))


def draw_room3(room):
    # Create the specific obstacles
    # Top left corner
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_START, TILE_SIZE * 4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * x, JAIL_Y_START))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START, JAIL_Y_START + TILE_SIZE))
    # Top right corner
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START, TILE_SIZE * 4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * (x + 9), JAIL_Y_START))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE))
    # Bot left corner
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE, TILE_SIZE * 4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * x, JAIL_Y_END - TILE_SIZE))
    barriers.add(Barrier(JAIL_X_START, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_START, JAIL_Y_END - TILE_SIZE * 2))
    # Bot right corner
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_END - TILE_SIZE, TILE_SIZE * 4, TILE_SIZE))
    for x in range(4):
        room.blit(basic_wall.convert(), (JAIL_X_START + TILE_SIZE * (9 + x), JAIL_Y_END - TILE_SIZE))
    barriers.add(Barrier(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE))
    room.blit(basic_wall.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE * 2))


def draw_room4(room):
    floor_gash.set_colorkey((255, 255, 255))
    # Create the specific obstacles
    # Top left
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE, JAIL_Y_START, TILE_SIZE * 2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * (1 + x), JAIL_Y_START))
    floor_gashes.add(FloorGash(JAIL_X_START, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START, JAIL_Y_START + TILE_SIZE))
    # Top right
    floor_gashes.add(FloorGash(JAIL_X_END - TILE_SIZE * 3, JAIL_Y_START, TILE_SIZE * 2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE * (2 + x), JAIL_Y_START))
    floor_gashes.add(FloorGash(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE))
    # Bottom left
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, TILE_SIZE * 2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * (1 + x), JAIL_Y_END - TILE_SIZE))
    floor_gashes.add(FloorGash(JAIL_X_START, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START, JAIL_Y_END - TILE_SIZE * 2))
    # Bottom right
    floor_gashes.add(FloorGash(JAIL_X_END - TILE_SIZE * 3, JAIL_Y_END - TILE_SIZE, TILE_SIZE * 2, TILE_SIZE))
    for x in range(2):
        room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE * (2 + x), JAIL_Y_END - TILE_SIZE))
    floor_gashes.add(FloorGash(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE * 2))


def draw_room5(room):
    floor_gash.set_colorkey((255, 255, 255))

    # Middle island
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 5, JAIL_Y_START + TILE_SIZE * 2, TILE_SIZE * 3, TILE_SIZE))
    for x in range(3):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * (5 + x), JAIL_Y_START + TILE_SIZE * 2))
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 5, JAIL_Y_START + TILE_SIZE * 4, TILE_SIZE * 3, TILE_SIZE))
    for x in range(3):
        room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * (5 + x), JAIL_Y_START + TILE_SIZE * 4))
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3))
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3))


# def draw_room6(room):

# def draw_boss_room1(room):

# def draw_boss_room2(room):

# def draw_final_boss(room):


def room_choice(background, num):
    """randomise room choice"""
    if num == 0:
        draw_room0(background)
    elif num == 1:
        draw_room1(background)
    elif num == 2:
        draw_room2(background)
    elif num == 3:
        draw_room3(background)
    elif num == 4:
        draw_room4(background)
    elif num == 5:
        draw_room5(background)
