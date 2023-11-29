import pygame
from game_parameters import *
import math
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.forward_image = pygame.transform.scale(
            pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0112.png").convert(),
            (28, 28))
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

    def update(self, barriers, floor_gashes):
        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_a] and self.rect.left > JAIL_X_START:
            self.rect.x += -self.spd
        if KEYS[pygame.K_d] and self.rect.right < JAIL_X_END:
            self.rect.x += self.spd
        if KEYS[pygame.K_w] and self.rect.top > JAIL_Y_START:
            self.rect.y += -self.spd
        if KEYS[pygame.K_s] and self.rect.bottom < JAIL_Y_END:
            self.rect.y += self.spd

        # Check for collisions with barriers
        collisions = pygame.sprite.spritecollide(self, barriers, False)
        for barrier in collisions:
            if KEYS[pygame.K_a] and self.rect.left < barrier.rect.right:
                self.rect.left = barrier.rect.right
            if KEYS[pygame.K_d] and self.rect.right > barrier.rect.left:
                self.rect.right = barrier.rect.left
            if KEYS[pygame.K_w] and self.rect.top < barrier.rect.bottom:
                self.rect.top = barrier.rect.bottom
            if KEYS[pygame.K_s] and self.rect.bottom > barrier.rect.top:
                self.rect.bottom = barrier.rect.top

        # Check for collisions with floor_gashes
        collisions = pygame.sprite.spritecollide(self, floor_gashes, False)
        for floor_gash in collisions:
            if KEYS[pygame.K_a] and self.rect.left < floor_gash.rect.right:
                self.rect.left = floor_gash.rect.right
            if KEYS[pygame.K_d] and self.rect.right > floor_gash.rect.left:
                self.rect.right = floor_gash.rect.left
            if KEYS[pygame.K_w] and self.rect.top < floor_gash.rect.bottom:
                self.rect.top = floor_gash.rect.bottom
            if KEYS[pygame.K_s] and self.rect.bottom > floor_gash.rect.top:
                self.rect.bottom = floor_gash.rect.top

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Knife(pygame.sprite.Sprite):
    #this code I got the base from Will and made some adjustments for my game
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0103.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = BASE_KNIFE_SPD
        self.start_x = start_x
        self.start_y = start_y

    def update(self, barriers):
        # Calculate the angle between the projectile and the target
        angle = math.atan2(self.target_y - self.start_y, self.target_x - self.start_x)

        # Calculate the velocity components
        velocity_x = self.speed * math.cos(angle)
        velocity_y = self.speed * math.sin(angle)

        # Update the projectile's position based on velocity
        self.rect.x += velocity_x
        self.rect.y += velocity_y

        #TODO: kill the knives when they hit the side of the jail or if they get out of range
        if (self.rect.right > JAIL_X_END or self.rect.left < JAIL_X_START
                or self.rect.bottom > JAIL_Y_END or self.rect.top < JAIL_Y_START
                or abs(self.rect.x - self.start_x) > TILE_SIZE*BASE_ATK_RNG or
                abs(self.rect.y - self.start_y) > TILE_SIZE*BASE_ATK_RNG):
            self.kill()


    def draw(self, surface):
        surface.blit(self.image, self.rect.center)

knives = pygame.sprite.Group()
