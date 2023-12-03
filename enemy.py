import pygame
import random
from game_parameters import *
from objects import barriers, floor_gashes
import math


class Guard(pygame.sprite.Sprite):
    def __init__(self, x, y, target, spd=GUARD_SPD, atk=GUARD_ATK, hp=GUARD_HP):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0096.png").convert(),
            (28, 28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.spd = spd
        self.hp = hp
        self.atk = atk
        self.target = target
        self.rect.topleft = (x, y)
        self.x_move = 0     # Only used to see if it is moving or not
        self.y_move = 0     # Only used to see if it is moving or not

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Got this code from will
    def update(self, barrier, floor_gash):
        if self.rect.x != self.target.rect.x or self.rect.y != self.target.rect.y:
            try:
                self.rect.x += (self.target.rect.x - self.rect.x)/abs(self.target.rect.x - self.rect.x) * GUARD_SPD
                self.rect.y += (self.target.rect.y - self.rect.y)/abs(self.target.rect.y - self.rect.y) * GUARD_SPD
                self.x_move = 1
                self.y_move = 1
            except ZeroDivisionError:
                try:
                    self.rect.y += (self.target.rect.y - self.rect.y)/abs(self.target.rect.y - self.rect.y) * GUARD_SPD
                    self.x_move = 0
                    self.y_move = 1
                except ZeroDivisionError:
                    self.x_move = 0
                    self.y_move = 0
                    pass

        # check for collision with barriers
        collisions = pygame.sprite.spritecollide(self, barriers, False)
        if sum([self.x_move, self.y_move]) == 1:
            for barrier in collisions:
                if self.rect.left < barrier.rect.right:
                    self.rect.left = barrier.rect.right
                if self.rect.right > barrier.rect.left:
                    self.rect.right = barrier.rect.left
                if self.rect.top < barrier.rect.bottom:
                    self.rect.top = barrier.rect.bottom
                if self.rect.bottom > barrier.rect.top:
                    self.rect.bottom = barrier.rect.top

        elif sum([self.x_move, self.y_move]) == 2:
            for barrier in collisions:
                if self.rect.left < barrier.rect.right:
                    self.rect.left = barrier.rect.right
                elif self.rect.right > barrier.rect.left:
                    self.rect.right = barrier.rect.left
                elif self.rect.top < barrier.rect.bottom:
                    self.rect.top = barrier.rect.bottom
                elif self.rect.bottom > barrier.rect.top:
                    self.rect.bottom = barrier.rect.top

        # Check for collision with floor_gashes
        collisions = pygame.sprite.spritecollide(self, floor_gashes, False)
        for floor_gash in collisions:
            if self.rect.left < floor_gash.rect.right:
                self.rect.left = floor_gash.rect.right
            if self.rect.right > floor_gash.rect.left:
                self.rect.right = floor_gash.rect.left
            if self.rect.top < floor_gash.rect.bottom:
                self.rect.top = floor_gash.rect.bottom
            if self.rect.bottom > floor_gash.rect.top:
                self.rect.bottom = floor_gash.rect.top


class Patrol(pygame.sprite.Sprite):
    def __init__(self, x, y, spd = PAT_SPD, atk = PAT_ATK, hp = PAT_HP):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0096.png").convert(),
            (28, 28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.spd = spd
        self.atk = atk
        self.hp = hp
        self.rect.topleft = (x, y)
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, barriers, floor_gashes):
        if self.direction == 'up':
            self.rect.y -= self.spd
            if self.rect.top < JAIL_Y_START:
                self.rect.top = JAIL_Y_START
                self.direction = random.choice(['down', 'left', 'right'])
        elif self.direction == 'down':
            self.rect.y += self.spd
            if self.rect.bottom > JAIL_Y_END:
                self.rect.bottom = JAIL_Y_END
                self.direction = random.choice(['up', 'left', 'right'])
        elif self.direction == 'left':
            self.rect.x -= self.spd
            if self.rect.left < JAIL_X_START:
                self.rect.left = JAIL_X_START
                self.direction = random.choice(['up', 'down', 'right'])
        elif self.direction == 'right':
            self.rect.x += self.spd
            if self.rect.right > JAIL_X_END:
                self.rect.right = JAIL_X_END
                self.direction = random.choice(['up', 'down', 'left'])

        collisions = pygame.sprite.spritecollide(self, barriers, False)
        for barrier in collisions:
            if self.rect.top < barrier.rect.bottom:
                self.rect.top = barrier.rect.bottom
                self.direction = random.choice(['down', 'left', 'right'])
            if self.rect.left < barrier.rect.right:
                self.rect.left = barrier.rect.right
                self.direction = random.choice(['up', 'down', 'right'])
            if self.rect.bottom > barrier.rect.top:
                self.rect.bottom = barrier.rect.top
                self.direction = random.choice(['up', 'right', 'left'])
            if self.rect.right > barrier.rect.left:
                self.rect.right = barrier.rect.left
                self.direction = random.choice(['up', 'down', 'left'])

        collisions = pygame.sprite.spritecollide(self, floor_gashes, False)
        for floor_gash in collisions:
            if self.rect.top < floor_gash.rect.bottom:
                self.rect.top = floor_gash.rect.bottom
                self.direction = random.choice(['down', 'left', 'right'])
            if self.rect.left < floor_gash.rect.right:
                self.rect.left = floor_gash.rect.right
                self.direction = random.choice(['up', 'down', 'right'])
            if self.rect.bottom > floor_gash.rect.top:
                self.rect.bottom = floor_gash.rect.top
                self.direction = random.choice(['up', 'right', 'left'])
            if self.rect.right > floor_gash.rect.left:
                self.rect.right = floor_gash.rect.left
                self.direction = random.choice(['up', 'down', 'left'])


class Sentry(pygame.sprite.Sprite):
    def __init__(self, x, y, atk = SENTRY_ATK, hp = SENTRY_HP):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0098.png").convert(),
            (28, 28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.atk = atk
        self.hp = hp
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# for ranged enemies to use


class Arrow(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0131.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = BASE_KNIFE_SPD
        self.start_x = start_x
        self.start_y = start_y

    def update(self):
        # Calculate the angle between the projectile and the target
        angle = math.atan2(self.target_y - self.start_y, self.target_x - self.start_x)

        # Calculate the velocity components
        velocity_x = self.speed * math.cos(angle)
        velocity_y = self.speed * math.sin(angle)

        # Update the projectile's position based on velocity
        self.rect.x += velocity_x
        self.rect.y += velocity_y

        if (self.rect.right > JAIL_X_END or self.rect.left < JAIL_X_START
                or self.rect.bottom > JAIL_Y_END or self.rect.top < JAIL_Y_START):
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Broken_Prisoner(pygame.sprite.Sprite):
    def __init__(self, x, y, spd = PAT_SPD, atk = PAT_ATK, hp = PAT_HP):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0088.png").convert(),
            (28, 28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.spd = spd
        self.atk = atk
        self.hp = hp
        self.rect.topleft = (x, y)
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, barriers, floor_gashes):
        # Choose a random direction
        direction = random.choice(['up', 'down', 'left', 'right'])

        # Move the sprite based on the chosen direction
        if direction == 'up':
            self.rect.centery -= self.spd
            if self.rect.top < JAIL_Y_START:
                self.rect.top = JAIL_Y_START
        elif direction == 'down':
            self.rect.centery += self.spd
            if self.rect.bottom > JAIL_Y_END:
                self.rect.bottom = JAIL_Y_END
        elif direction == 'left':
            self.rect.centerx -= self.spd
            if self.rect.left < JAIL_X_START:
                self.rect.left = JAIL_X_START
        elif direction == 'right':
            self.rect.centerx += self.spd
            if self.rect.right > JAIL_X_END:
                self.rect.right = JAIL_X_END

        collisions = pygame.sprite.spritecollide(self, barriers, False)
        for barrier in collisions:
            if self.rect.top < barrier.rect.bottom:
                self.rect.top = barrier.rect.bottom
            if self.rect.left < barrier.rect.right:
                self.rect.left = barrier.rect.right
            if self.rect.bottom > barrier.rect.top:
                self.rect.bottom = barrier.rect.top
            if self.rect.right > barrier.rect.left:
                self.rect.right = barrier.rect.left

        collisions = pygame.sprite.spritecollide(self, floor_gashes, False)
        for floor_gash in collisions:
            if self.rect.top < floor_gash.rect.bottom:
                self.rect.top = floor_gash.rect.bottom
            if self.rect.left < floor_gash.rect.right:
                self.rect.left = floor_gash.rect.right
            if self.rect.bottom > floor_gash.rect.top:
                self.rect.bottom = floor_gash.rect.top
            if self.rect.right > floor_gash.rect.left:
                self.rect.right = floor_gash.rect.left


guards = pygame.sprite.Group()
patrols = pygame.sprite.Group()
sentries = pygame.sprite.Group()
arrows = pygame.sprite.Group()
broken_prisoners = pygame.sprite.Group()

enemies = [guards, patrols, sentries, broken_prisoners]
