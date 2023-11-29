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

class Floor_Gash(pygame.sprite.Sprite):
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
doors = pygame.sprite.Group()

#doors.add()