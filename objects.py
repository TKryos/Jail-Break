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

class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(Hitbox_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



door_top = Door(SCREEN_WIDTH/2 - TILE_SIZE, JAIL_Y_START-TILE_SIZE, TILE_SIZE * 2, TILE_SIZE)
door_left = Door(JAIL_X_START - TILE_SIZE, SCREEN_HEIGHT/2 - TILE_SIZE, TILE_SIZE, TILE_SIZE * 2)
door_right = Door(JAIL_X_END, SCREEN_HEIGHT/2 - TILE_SIZE, TILE_SIZE, TILE_SIZE * 2)
door_bot = Door(SCREEN_WIDTH/2 - TILE_SIZE, JAIL_Y_END, TILE_SIZE * 2, TILE_SIZE)

barriers = pygame.sprite.Group()
holes = pygame.sprite.Group()
doors = pygame.sprite.Group()

doors.add(door_top, door_left, door_right, door_bot)