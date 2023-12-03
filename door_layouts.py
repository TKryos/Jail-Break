import pygame
from game_parameters import *
from tiles_etc import (boss_door_indicators, item_door_indicators,
                       door_closed, door_open, stair_image)
from objects import (top_doors, left_doors, right_doors, bot_doors,
                     door_top, door_left, door_right, door_bot,
                     stairs, stair)


def draw_closed_boss_door_top(room):
    room.blit(boss_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_START - TILE_SIZE))
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE))
    room.blit(boss_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_START - TILE_SIZE))


def draw_closed_boss_door_bot(room):
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_END))


def draw_closed_boss_door_left(room):
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 4))


def draw_closed_boss_door_right(room):
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 4))


def draw_open_boss_door_top(room):
    top_doors.add(door_top)
    room.blit(boss_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_START - TILE_SIZE))
    room.blit(door_open.convert(),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE))
    room.blit(boss_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_START - TILE_SIZE))


def draw_open_boss_door_bot(room):
    bot_doors.add(door_bot)
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_open.convert(), 180),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_END))


def draw_open_boss_door_left(room):
    left_doors.add(door_left)
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_open.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 4))


def draw_open_boss_door_right(room):
    right_doors.add(door_right)
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_open.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(boss_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 4))


def draw_closed_item_door_top(room):
    room.blit(item_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_START - TILE_SIZE))
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE))
    room.blit(item_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_START - TILE_SIZE))


def draw_closed_item_door_bot(room):
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_END))


def draw_closed_item_door_left(room):
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 4))


def draw_closed_item_door_right(room):
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 4))


def draw_open_item_door_top(room):
    top_doors.add(door_top)
    room.blit(item_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_START - TILE_SIZE))
    room.blit(door_open.convert(),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE))
    room.blit(item_door_indicators.convert(),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_START - TILE_SIZE))


def draw_open_item_door_bot(room):
    bot_doors.add(door_bot)
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*5, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_open.convert(), 180),
              (JAIL_X_START + TILE_SIZE*6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 180),
              (JAIL_X_START + TILE_SIZE*7, JAIL_Y_END))


def draw_open_item_door_left(room):
    left_doors.add(door_left)
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_open.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 4))


def draw_open_item_door_right(room):
    right_doors.add(door_right)
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 2))
    room.blit(pygame.transform.rotate(door_open.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(item_door_indicators.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 4))


def draw_closed_doors(room):
    # doors.add(door_top, door_left, door_right, door_bot)
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),   # Left side
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),  # Right side
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))


def draw_right_closed_door(room):
    room.blit(pygame.transform.rotate(door_closed.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))


def draw_left_closed_door(room):
    room.blit(pygame.transform.rotate(door_closed.convert(), 90),  # Left side
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))


def draw_top_closed_door(room):
    room.blit(door_closed.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))


def draw_bot_closed_door(room):
    room.blit(pygame.transform.rotate(door_closed.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))


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


def draw_top_open_door(room):
    top_doors.add(door_top)
    room.blit(door_open.convert(),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START - TILE_SIZE))


def draw_bot_open_door(room):
    bot_doors.add(door_bot)
    room.blit(pygame.transform.rotate(door_open.convert(), 180),
              (JAIL_X_START + TILE_SIZE * 6, JAIL_Y_END))


def draw_left_open_door(room):
    left_doors.add(door_left)
    room.blit(pygame.transform.rotate(door_open.convert(), 90),
              (JAIL_X_START - TILE_SIZE, JAIL_Y_START + TILE_SIZE * 3))


def draw_right_open_door(room):
    right_doors.add(door_right)
    room.blit(pygame.transform.rotate(door_open.convert(), 270),
              (JAIL_X_END, JAIL_Y_START + TILE_SIZE * 3))


def draw_stairs(room):
    stairs.add(stair)
    room.blit(stair_image, (JAIL_X_START + TILE_SIZE*5, JAIL_Y_START))