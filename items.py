import pygame
from tiles_etc import health_pot, maxhpup, atkup, atkrngup, atkspdup, spdup, knifespdup


class HealthPot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = health_pot.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class SpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = spdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkspdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class KnifeSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = knifespdup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MaxHpUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = maxhpup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class RngUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = atkrngup.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)

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
