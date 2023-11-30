import pygame

# TODO: find images and make the interactions for each item


class SpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class KnifeSpdUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class HpUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AtkUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class RngUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)