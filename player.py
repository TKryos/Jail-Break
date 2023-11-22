import pygame
from game_parameters import *
from objects import barriers, Barrier
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.forward_image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0112.png")
        self.reverse_image = pygame.transform.flip(self.forward_image, True, False)
        self.image = self.forward_image
        self.rect = self.image.get_rect()
        self.x = x                  #defines x pos
        self.y = y                  #defines y pos
        self.rect.center = (x,y)
        self.x_spd = 0              #defines movement in the x
        self.y_spd = 0              #defines movement in the y
        self.atk = BASE_ATK         #defines attack power
        self.atk_spd = BASE_ATK_SPD #defines attack speed
        self.spd = BASE_SPD         #defines movement speed
        self.hp = BASE_HP           #defines health pool

    def update(self, barriers):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > JAIL_X_START:
            self.rect.x -= self.spd
        if keys[pygame.K_d] and self.rect.right < JAIL_X_END:
            self.rect.x += self.spd
        if keys[pygame.K_w] and self.rect.top > JAIL_Y_START:
            self.rect.y -= self.spd
        if keys[pygame.K_s] and self.rect.bottom < JAIL_Y_END:
            self.rect.y += self.spd

        # Check for collisions with barriers
        collisions = pygame.sprite.spritecollide(self, barriers, False)
        for barrier in collisions:
            if keys[pygame.K_a] and self.rect.left < barrier.rect.right:
                self.rect.left = barrier.rect.right
            if keys[pygame.K_d] and self.rect.right > barrier.rect.left:
                self.rect.right = barrier.rect.left
            if keys[pygame.K_w] and self.rect.top < barrier.rect.bottom:
                self.rect.top = barrier.rect.bottom
            if keys[pygame.K_s] and self.rect.bottom > barrier.rect.top:
                self.rect.bottom = barrier.rect.top


    def draw(self, surface):
        surface.blit(self.image, self.rect)

