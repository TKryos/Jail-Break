import pygame

#TODO: find images and make the interactions for each item
class spd_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class atk_spd_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class knife_spd_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class hp_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class atk_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        # self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class rng_up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image =
        #self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)