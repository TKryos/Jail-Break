#import pygame
#import random
#
#
## Initialize Pygame
#pygame.init()
#
## Constants
#WIDTH, HEIGHT = 800, 600
#FPS = 60
#
## Colors
#WHITE = (255, 255, 255)
#RED = (255, 0, 0)
#
## Sprite class
#class Sprite(pygame.sprite.Sprite):
#    def __init__(self):
#        super().__init__()
#        self.image = pygame.Surface((50, 50))
#        self.image.fill(RED)
#        self.rect = self.image.get_rect()
#        self.rect.center = (WIDTH // 2, HEIGHT // 2)
#        self.speed = 5
#        self.direction = random.choice(['up', 'down', 'left', 'right'])
#
#    def update(self):
#        if self.direction == 'up':
#            self.rect.y -= self.speed
#        elif self.direction == 'down':
#            self.rect.y += self.speed
#        elif self.direction == 'left':
#            self.rect.x -= self.speed
#        elif self.direction == 'right':
#            self.rect.x += self.speed
#
#        #restrict movement to within the screen
#        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
#        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))
#
#        # Check if sprite has reached the screen boundaries
#        if self.rect.top <= 1 or self.rect.bottom >= HEIGHT - 1 or self.rect.left <= 1 or self.rect.right >= WIDTH - 1:
#            # If yes, choose a new random direction
#            self.direction = random.choice(['up', 'down', 'left', 'right'])
#
## Initialize Pygame window
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Random Direction Sprite")
#clock = pygame.time.Clock()
#
#all_sprites = pygame.sprite.Group()
#sprite = Sprite()
#all_sprites.add(sprite)
#
## Game loop
#running = True
#while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#
#    # Update
#    all_sprites.update()
#
#    # Draw / Render
#    screen.fill(WHITE)
#    all_sprites.draw(screen)
#
#    # Flip the display
#    pygame.display.flip()
#
#    # Cap the frame rate
#    clock.tick(FPS)
#
## Quit Pygame
#pygame.quit()

import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0
                self.direction = random.choice(['down', 'left', 'right'])
        elif self.direction == 'down':
            self.rect.y += self.speed
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.direction = random.choice(['up', 'left', 'right'])
        elif self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
                self.direction = random.choice(['up', 'down', 'right'])
        elif self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.direction = random.choice(['up', 'down', 'left'])

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move Along Wall Sprite")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
sprite = Sprite()
all_sprites.add(sprite)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()