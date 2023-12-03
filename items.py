import pygame
from tiles_etc import health_pot, maxhpup, atkup, atkrngup, atkspdup, spdup, knifespdup
from game_parameters import *


class HealthPot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = health_pot.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class SpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = spdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkspdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class KnifeSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = knifespdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MaxHpUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = maxhpup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class RngUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkrngup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


hp_pots = pygame.sprite.Group()

spd_boosts = pygame.sprite.Group()
atk_spd_boosts = pygame.sprite.Group()
knife_spd_boosts = pygame.sprite.Group()
max_hp_boosts = pygame.sprite.Group()
atk_boosts = pygame.sprite.Group()
rng_boosts = pygame.sprite.Group()
items = [spd_boosts, atk_spd_boosts, knife_spd_boosts, max_hp_boosts, atk_boosts, rng_boosts]

def item_choice(item_num, surface):
    if item_num == 0:
        spd_boosts.add(SpdUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        spd_boosts.draw(surface)
    if item_num == 1:
        atk_spd_boosts.add(AtkSpdUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        atk_spd_boosts.draw(surface)
    if item_num == 2:
        knife_spd_boosts.add(KnifeSpdUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        knife_spd_boosts.draw(surface)
    if item_num == 3:
        max_hp_boosts.add(MaxHpUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        max_hp_boosts.draw(surface)
    if item_num == 4:
        atk_boosts.add(AtkUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        atk_boosts.draw(surface)
    if item_num == 5:
        rng_boosts.add(RngUp(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        rng_boosts.add(surface)

def pots1(con, surface):
    if con == 0:
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE * 3))
        for pot in hp_pots:
            pot.draw(surface)
    if con == 1:
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE * 3))
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE * 3))
        for pot in hp_pots:
            pot.draw(surface)
    else:
        pass

def pots2(pots, surface):
    if pots == 0:
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 6, JAIL_Y_START + TILE_SIZE))
        for pot in hp_pots:
            pot.draw(surface)

    if pots == 1:
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 3, JAIL_Y_START + TILE_SIZE))
        hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE * 9, JAIL_Y_START + TILE_SIZE))
