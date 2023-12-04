import pygame
from game_parameters import *
from objects import (top_doors, bot_doors, left_doors, right_doors, door_top, door_left, door_right, door_bot,
                     barriers, Barrier, floor_gashes, FloorGash)
from tiles_etc import (tutorial_font,basic_wall, floor_gash, stair_image,
                       door_open, door_closed, boss_door_indicators, item_door_indicators)
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
    """room that starts each floor"""
    pass

# TODO: make the possible instances for the door combinations(maybe) or make separate for top,left,right,down


# TODO: make the possible enemies for each room


def draw_room0(room):
    """Just an empty room"""
    pass


def r0_e1(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale))


def r0_e2(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE,  hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))


def r0_e3(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))


def r0_e4(player, scale = 1):
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*3, hp = BP_HP*scale))


def r0_e5(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
    guards.add(Guard(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*3, player, hp = GUARD_HP*scale))

def r0_e6(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))
    guards.add(Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale))
def draw_room1(room):
    """Large wall in the middle"""
    # Create the specific obstacles
    barriers.add(Barrier(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 2, TILE_SIZE * 7, TILE_SIZE * 3))
    for x in range(JAIL_X_START + TILE_SIZE * 3, JAIL_X_END - TILE_SIZE * 3, TILE_SIZE):
        for y in range(JAIL_Y_START + TILE_SIZE * 2, JAIL_Y_END - TILE_SIZE * 2, TILE_SIZE):
            room.blit(basic_wall, (x, y))


# The parenthesis can house the enemy stats if wanted

def r1_e1(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale))


def r1_e2(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))


def r1_e3(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))


def r1_e4(player, scale = 1):
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))


def r1_e5(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))


def r1_e6(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale))


def draw_room2(room):
    """Scattered Rocks"""
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


def r2_e1(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
def r2_e2(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))

def r2_e3(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))

def r2_e4(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale))

def r2_e5(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale),
                Guard(JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))


def draw_room3(room):
    """Holes in corners"""
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

def r3_e1(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START, JAIL_Y_START, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
    guards.add(Guard(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale),
                Guard(JAIL_X_END - TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale))

def r3_e2(player, scale = 1):
    sentries.add(Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
    guards.add(Guard(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale),
                Guard(JAIL_X_END - TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale))

def r3_e3(player, scale = 1):
    sentries.add(Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START, JAIL_Y_START, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
def draw_room4(room):
    """Center island defined by floor gashes"""
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

def r4_e1(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale))
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))

def r4_e2(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE*5, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE*7, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))

def r4_e3(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale))

def r4_e4(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))

def r4_e5(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE*5, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE*7, JAIL_Y_START + TILE_SIZE*3, hp = SENTRY_HP*scale))
    guards.add(Guard(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale),
                Guard(JAIL_X_END - TILE_SIZE*2, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale))
def draw_room5(room):
    """Scattered Holes"""
    floor_gash.set_colorkey((255, 255, 255))

    # Create the specific obstacles
    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 1, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 1, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 5, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 5))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 5, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 5))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 1, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))

    floor_gashes.add(FloorGash(JAIL_X_START + TILE_SIZE * 11, JAIL_Y_START + TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
    room.blit(floor_gash.convert(), (JAIL_X_START + TILE_SIZE * 11, JAIL_Y_START + TILE_SIZE * 3))


def r5_e1(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = SENTRY_HP*scale))


def r5_e2(player, scale = 1):
    sentries.add(Sentry(JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3, hp = SENTRY_HP*scale),
                 Sentry(JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3, hp = SENTRY_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))


def r5_e3(player, scale = 1):
    patrols.add(Patrol(JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = PAT_HP*scale),
                Patrol(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = PAT_HP*scale))


def r5_e4(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, player, hp = GUARD_HP*scale))


def r5_e5(player, scale = 1):
    guards.add(Guard(JAIL_X_START + TILE_SIZE * 4, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale),
               Guard(JAIL_X_START + TILE_SIZE * 8, JAIL_Y_START + TILE_SIZE * 3, player, hp = GUARD_HP*scale))
    broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_START + TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_START + TILE_SIZE, hp = BP_HP*scale),
                         Broken_Prisoner(JAIL_X_END - TILE_SIZE, JAIL_Y_END - TILE_SIZE, hp = BP_HP*scale))
def room_choice(background, room, enemy, player, scale = 1):
    """randomize room choice"""
    if room == 0:
        draw_room0(background)
        if enemy == 0:
            pass
        elif enemy == 1:
            r0_e1(player, scale)
        elif enemy == 2:
            r0_e2(player, scale)
        elif enemy == 3:
            r0_e3(player, scale)
        elif enemy == 4:
            r0_e4(player, scale)
        elif enemy == 5:
            r0_e5(player, scale)
        elif enemy == 6:
            r0_e6(player, scale)

    elif room == 1:
        draw_room1(background)
        if enemy == 0:
            pass
        elif enemy == 1:
            r1_e1(player, scale)
        elif enemy == 2:
            r1_e2(player, scale)
        elif enemy == 3:
            r1_e3(player, scale)
        elif enemy == 4:
            r1_e4(player, scale)
        elif enemy == 5:
            r1_e5(player, scale)
        elif enemy == 6:
            r1_e6(player, scale)

    elif room == 2:
        draw_room2(background)
        if enemy == 0:
            pass
        elif enemy == 1:
            r2_e1(player, scale)
        elif enemy == (2 or 6):
            r2_e2(player, scale)
        elif enemy == 3:
            r2_e3(player, scale)
        elif enemy == 4:
            r2_e4(player, scale)
        elif enemy == 5:
            r2_e5(player, scale)

    elif room == 3:
        draw_room3(background)
        if enemy == 0:
            pass
        elif enemy == (6 or 3):
            r3_e1(player, scale)
        elif enemy == (1 or 4):
            r3_e2(player, scale)
        elif enemy == (2 or 5):
            r3_e3(player, scale)


    elif room == 4:
        draw_room4(background)
        if enemy == 0:
            pass
        if enemy == 6:
            r4_e1(player, scale)
        elif enemy == 1:
            r4_e2(player, scale)
        elif enemy == 2:
            r4_e3(player, scale)
        elif enemy == (3 or 5):
            r4_e4(player, scale)
        elif enemy == 4:
            r4_e5(player, scale)

    elif room == 5:
        draw_room5(background)
        if enemy == 0:
            pass
        elif enemy == 6:
            r5_e1(player, scale)
        elif enemy == (1 or 5):
            r5_e2(player, scale)
        elif enemy == 2:
            r5_e3(player, scale)
        elif enemy == 3:
            r5_e4(player, scale)
        elif enemy == 4:
            r5_e5(player, scale)
