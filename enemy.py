import pygame
import random
from game_parameters import *
from objects import barriers

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x                      #defines x pos
        self.y = y                      #defines y pos
        self.x_spd = 0                  #defines movement in the x
        self.y_spd = 0                  #defines movement in the y

    def move_up(self):
        self.y_spd = PAT_SPD

    def move_left(self):
        self.x_spd = -1 * PAT_SPD

    def move_down(self):
        self.y_spd = -1 * PAT_SPD

    def move_right(self):
        self.x_spd = PAT_SPD

    def update(self):
        self.x += self.x_spd

        self.y += self.y_spd

class Guard(pygame.sprite.Sprite):
    def __init__(self,x,y,target, spd = GUARD_SPD, atk = GUARD_ATK, hp = GUARD_HP):
        super().__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0096.png").convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.spd = spd
        self.hp = hp
        self.atk = atk
        self.target = target
        self.rect.center = (x,y)
        self.x_speed = 0
        self.y_speed = 0

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def update(self, barrier):
        if self.rect.x != self.target.rect.x or self.rect.y != self.target.rect.y:
            try:
                self.rect.x += (self.target.rect.x - self.rect.x)/abs(self.target.rect.x - self.rect.x) * GUARD_SPD
                self.rect.y += (self.target.rect.y - self.rect.y)/abs(self.target.rect.y - self.rect.y) * GUARD_SPD
            except ZeroDivisionError:
                try:
                    self.rect.y += (self.target.rect.y - self.rect.y)/abs(self.target.rect.y - self.rect.y) * GUARD_SPD
                except:
                    pass
        collisions = pygame.sprite.spritecollide(self, barriers, False)
        for barrier in collisions:
            if self.rect.left < barrier.rect.right:
                self.rect.left = barrier.rect.right
            if self.rect.right > barrier.rect.left:
                self.rect.right = barrier.rect.left
            if self.rect.top < barrier.rect.bottom:
                self.rect.top = barrier.rect.bottom
            if self.rect.bottom > barrier.rect.top:
                self.rect.bottom = barrier.rect.top

class Patrol(pygame.sprite.Sprite):
    def __init__(self, x, y, spd = PAT_SPD, atk = PAT_ATK, hp = PAT_HP):
        super.__init__()
        #TODO: find sprite
        self.x = x
        self.y = y
        self.x_spd = spd
        self.y_spd = spd
        self.atk = atk
        self.hp = hp

    def move_up(self):
        self.y_spd = PAT_SPD

    def move_left(self):
        self.x_spd = -1 * PAT_SPD

    def move_down(self):
        self.y_spd = -1 * PAT_SPD

    def move_right(self):
        self.x_spd = PAT_SPD



class Sentry(Enemy):
    def __init__(self, x, y, spd = SENTRY_SPD, atk = SENTRY_ATK, hp = SENTRY_HP):
        super.__init__()
        #TODO: find sprite
        self.x = x
        self.y = y
        self.x_spd = spd
        self.y_spd = spd
        self.atk = atk
        self.hp = hp

class Coward(Enemy):
    def __init__(self, x, y, spd, atk, hp):
        super.__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0096.png").convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.x_spd = spd
        self.y_spd = spd
        self.atk = atk
        self.hp = hp

class Broken_Prisoner(pygame.sprite.Sprite):
    #TODO: make it interact with barriers
    def __init__(self, x, y, spd = PAT_SPD, atk = PAT_ATK, hp = PAT_HP):
        super().__init__()
        self.image = pygame.image.load("assets/kenney_tiny-dungeon/Tiles/tile_0096.png").convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.spd = spd
        self.atk = atk
        self.hp = hp
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
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
enemies = pygame.sprite.Group()