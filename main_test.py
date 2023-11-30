import pygame
import random
import math
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_open_doors, draw_closed_doors,
                   draw_room0, draw_room1, draw_room2, draw_room3, draw_room4, draw_room5, room_choice,
                   r1_e1, r1_e2, r1_e3, r1_e4)
from background import draw_background
from player import Player, Knife, knives
from enemy import (Guard, Sentry, Patrol, Broken_Prisoner,
                   guards, sentries, patrols, broken_prisoners, Arrow, arrows, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash)


#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()

#overall background
draw_background(background)
draw_room0(background)
draw_open_doors(background)
#room_choice(background)

#create the player
player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

hearts = pygame.image.load("assets/tiles/heart.png").convert()
hearts.set_colorkey((255,255,255))

#create the enemies
r1_e4(player)
#patrols.add(Patrol(JAIL_X_START + TILE_SIZE * 2, JAIL_Y_START + TILE_SIZE * 2))
#guards.add(Guard(JAIL_X_START + TILE_SIZE, JAIL_Y_START + TILE_SIZE, player))
#sentries.add(Sentry(JAIL_X_START + 16, JAIL_Y_START + 16))
#broken_prisoners.add(Broken_Prisoner(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE*2))

#clock object
clock = pygame.time.Clock()

#make two boxes on the left and right of the screen to start or quit game
#Play = title_font.render("Jail-Break!", True, (0, 0, 0))
#Exit = title_font.render("Exit Game", True, (0, 0, 0))
#background.blit(Play, (50, SCREEN_HEIGHT//2 - Play.get_height()//2))
#background.blit(Exit, (SCREEN_WIDTH - int(Exit.get_width()) - 50, SCREEN_HEIGHT//2 - Play.get_height()//2))

print(player.hp)

#Main Loop
running = True
while running and player.hp > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


####This is all code that is going into every floor/room

    ####This is for throwing knives
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            knife = Knife(player.rect.centerx, player.rect.centery, *event.pos, player.rng)

        ####code to limit how often you can throw knives
            current_time = pygame.time.get_ticks()
            if current_time - LAST_THROW_TIME >= player.atk_spd:
                knives.add(knife)
                LAST_THROW_TIME = current_time
####code to randomly decide when a sentry fires an arrow
    for sentry in sentries:

        chance = random.randint(0, 60)
        if chance == 1:
            arrows.add(Arrow(sentry.rect.centerx, sentry.rect.centery, player.rect.centerx, player.rect.centery))

####code to check for damage from different enemies and limit how often you can take damage
    if pygame.sprite.spritecollide(player, guards, False):
        current_time = pygame.time.get_ticks()
        if current_time - LAST_DMG_TIME >= 1000:
            player.hp -= GUARD_ATK
            LAST_DMG_TIME = current_time

    if pygame.sprite.spritecollide(player, patrols, False):
        current_time = pygame.time.get_ticks()
        if current_time - LAST_DMG_TIME >= 1000:
            player.hp -= PAT_ATK
            LAST_DMG_TIME = current_time

    if pygame.sprite.spritecollide(player, sentries, False):
        current_time = pygame.time.get_ticks()
        if current_time - LAST_DMG_TIME >= 1000:
            player.hp -= SENTRY_ATK
            LAST_DMG_TIME = current_time

    if pygame.sprite.spritecollide(player, broken_prisoners, False):
        current_time = pygame.time.get_ticks()
        if current_time - LAST_DMG_TIME >= 1000:
            player.hp -= BP_ATK
            LAST_DMG_TIME = current_time


    if pygame.sprite.spritecollide(player, arrows, True):
        current_time = pygame.time.get_ticks()
        if current_time - LAST_DMG_TIME >= 1000:
            player.hp -= ARROW_ATK
            LAST_DMG_TIME = current_time

####Code that checks if enemies collide with knives and deals damage to them
    for group in enemies:
        for enemy in group:
            if pygame.sprite.spritecollide(enemy, knives, True):
                enemy.hp -= player.atk
            ####if enemy hp drops to or below 0, it kills the sprite
                if enemy.hp <= 0:
                    enemy.kill()
    LIVES = player.hp
####This is all code that is going into every floor/room

    #draw background
    screen.blit(background, (0,0))

    #update player location
    player.update(barriers, floor_gashes)
    guards.update(barriers, floor_gashes)
    patrols.update(barriers, floor_gashes)
    broken_prisoners.update(barriers, floor_gashes)
    arrows.update()
    knives.update(barriers)



    #draw game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
#    guards.draw(screen)
#    patrols.draw(screen)
#    sentries.draw(screen)
    arrows.draw(screen)
#    broken_prisoners.draw(screen)
    knives.draw(screen)

    for i in range(player.hp):
        if i <= 9:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-1), JAIL_Y_END + TILE_SIZE))
        elif i <= 19:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-11), JAIL_Y_END + TILE_SIZE*2))
        elif i <= 29:
            screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-21), JAIL_Y_END + TILE_SIZE*3))
    #update the display
    pygame.display.flip()

    #limit the fps
    clock.tick(30)

#quit pygame
pygame.quit()
sys.exit()