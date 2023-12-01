import pygame
from game_parameters import *

Hitbox_color = (140, 140, 0)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class FloorGash(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class DoorT(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class DoorL(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class DoorR(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class DoorB(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


door_top = DoorT(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START - TILE_SIZE + 1, TILE_SIZE, TILE_SIZE)
door_left = DoorL(JAIL_X_START - TILE_SIZE + 1, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE)
door_right = DoorR(JAIL_X_END - 1, JAIL_Y_START + TILE_SIZE*3, TILE_SIZE, TILE_SIZE)
door_bot = DoorB(JAIL_X_START + TILE_SIZE*6, JAIL_Y_END - 1, TILE_SIZE, TILE_SIZE)

barriers = pygame.sprite.Group()
floor_gashes = pygame.sprite.Group()
top_doors = pygame.sprite.Group()
bot_doors = pygame.sprite.Group()
left_doors = pygame.sprite.Group()
right_doors = pygame.sprite.Group()

def clear_objects():
    for barrier in barriers:
        barriers.remove(barrier)
    for floor_gash in floor_gashes:
        floor_gashes.remove(floor_gash)
    for door in top_doors:
        top_doors.remove(door)
    for door in bot_doors:
        bot_doors.remove(door)
    for door in left_doors:
        left_doors.remove(door)
    for door in right_doors:
        right_doors.remove(door)
