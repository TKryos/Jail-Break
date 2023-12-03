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
        self.x = x                  # defines x pos
        self.y = y                  # defines y pos
        self.rect.center = (x, y)
        self.x_spd = 0                  # defines movement in the x
        self.y_spd = 0                  # defines movement in the y
        self.atk = BASE_ATK             ############# defines attack power
        self.atk_spd = BASE_ATK_SPD     ############# defines how often knives can be thrown
        self.knife_spd = BASE_KNIFE_SPD ############# defines how fast knives move
        self.rng = BASE_ATK_RNG         ############# defines how far knives are thrown
        self.spd = BASE_SPD             ############# defines movement speed
        self.hp = BASE_HP               ############# defines health available
        self.maxhp = BASE_MAX_HP            ############# defines total health pool

    def update(self, barriers, floor_gashes):
        KEYS = pygame.key.get_pressed()
        keyw, keya, keys, keyd = KEYS[pygame.K_w], KEYS[pygame.K_a], KEYS[pygame.K_s], KEYS[pygame.K_d]
        if keya and self.rect.left > JAIL_X_START:
            self.rect.x += -self.spd
        if keyd and self.rect.right < JAIL_X_END:
            self.rect.x += self.spd
        if keyw and self.rect.top > JAIL_Y_START:
            self.rect.y += -self.spd
        if keys and self.rect.bottom < JAIL_Y_END:
            self.rect.y += self.spd

        # Check for collisions with barriers
        collisions = pygame.sprite.spritecollide(self, barriers, False)
        if sum([keyw, keya, keys, keyd]) == 1:
            for barrier in collisions:
                if keya and self.rect.left < barrier.rect.right:
                    self.rect.left = barrier.rect.right
                if keyd and self.rect.right > barrier.rect.left:
                    self.rect.right = barrier.rect.left
                if keyw and self.rect.top < barrier.rect.bottom:
                    self.rect.top = barrier.rect.bottom
                if keys and self.rect.bottom > barrier.rect.top:
                    self.rect.bottom = barrier.rect.top
        if sum([keyw, keya, keys, keyd]) >= 2:
            for barrier in collisions:
                if KEYS[pygame.K_a] and self.rect.left < barrier.rect.right and (KEYS[pygame.K_w] or KEYS[pygame.K_s]):
                    self.rect.left = barrier.rect.right
                elif KEYS[pygame.K_d] and self.rect.right > barrier.rect.left and (KEYS[pygame.K_w] or KEYS[pygame.K_s]):
                    self.rect.right = barrier.rect.left

                # this is where the problem starts
                elif KEYS[pygame.K_w] and self.rect.top < barrier.rect.bottom and (KEYS[pygame.K_a] or KEYS[pygame.K_d]):
                    self.rect.top = barrier.rect.bottom
                elif KEYS[pygame.K_s] and self.rect.bottom > barrier.rect.top and (KEYS[pygame.K_a] or KEYS[pygame.K_d]):
                    self.rect.bottom = barrier.rect.top

        # Check for collisions with floor_gashes
        collisions = pygame.sprite.spritecollide(self, floor_gashes, False)
        if sum([keyw, keya, keys, keyd]) == 1:
            for floor_gash in collisions:
                if KEYS[pygame.K_a] and self.rect.left < floor_gash.rect.right:
                    self.rect.left = floor_gash.rect.right
                if KEYS[pygame.K_d] and self.rect.right > floor_gash.rect.left:
                    self.rect.right = floor_gash.rect.left
                if KEYS[pygame.K_w] and self.rect.top < floor_gash.rect.bottom:
                    self.rect.top = floor_gash.rect.bottom
                if KEYS[pygame.K_s] and self.rect.bottom > floor_gash.rect.top:
                    self.rect.bottom = floor_gash.rect.top

        if sum([keyw, keya, keys, keyd]) >= 2:
            for floor_gash in collisions:
                if KEYS[pygame.K_a] and self.rect.left < floor_gash.rect.right and (KEYS[pygame.K_w] or KEYS[pygame.K_s]):
                    self.rect.left = floor_gash.rect.right
                elif KEYS[pygame.K_d] and self.rect.right > floor_gash.rect.left and (
                        KEYS[pygame.K_w] or KEYS[pygame.K_s]):
                    self.rect.right = floor_gash.rect.left

                # this is where the problem starts
                elif KEYS[pygame.K_w] and self.rect.top < floor_gash.rect.bottom and (
                        KEYS[pygame.K_a] or KEYS[pygame.K_d]):
                    self.rect.top = floor_gash.rect.bottom
                elif (KEYS[pygame.K_s] and self.rect.bottom > floor_gash.rect.top and (
                        KEYS[pygame.K_a] or KEYS[pygame.K_d])):
                    self.rect.bottom = floor_gash.rect.top

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    # TODO: all of the stat boosts

    def health_potion(self, hp_pot):
        self.hp += hp_pot

    def max_hp_up(self, hp_boost):
        self.hp += hp_boost
        self.maxhp += hp_boost

    def atk_up(self, atk_boost):
        self.atk += atk_boost

    def atk_rng_up(self, atk_rng_boost):
        self.rng += atk_rng_boost

    def atk_spd_up(self, atk_spd_boost):
        self.atk_spd -= atk_spd_boost

    def knife_spd_up(self, knife_spd_boost):
        self.knife_spd += knife_spd_boost

    def spd_up(self, spd_boost):
        self.spd += spd_boost


class Knife(pygame.sprite.Sprite):
    # this code I got the base from Will and made some adjustments for my game
    def __init__(self, start_x, start_y, target_x, target_y, rng, speed):
        super().__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0103.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
        self.rng = rng
        self.speed = speed
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

        if (self.rect.right > JAIL_X_END or self.rect.left < JAIL_X_START
                or self.rect.bottom > JAIL_Y_END or self.rect.top < JAIL_Y_START
                or abs(self.rect.x - self.start_x) > TILE_SIZE//2*self.rng or
                abs(self.rect.y - self.start_y) > TILE_SIZE//2*self.rng):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect.center)


knives = pygame.sprite.Group()
