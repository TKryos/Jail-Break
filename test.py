import pygame
from game_parameters import *
from rooms import (draw_F1_start_room, draw_open_doors, draw_closed_doors,
                   draw_room1, draw_room2, draw_room3, draw_room4, draw_room5,
                   room_choice, r1_e1, r1_e2, r1_e3, r1_e4, )
from player import Player, knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, Floor_Gash)
from background import draw_background
import random

pygame.init()
# Init the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()
pygame.display.set_caption("Floor_1")


draw_background(background)

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

clock = pygame.time.Clock()
#make the possible rooms and their states
#room_c = draw_F1_start_room(background)
#room_c_state = 1
#
#room_l = room_choice(background)
#room_l_state = 0
#
#room_r = room_choice(background)
#room_r_state = 0
#
#room_u = room_choice(background)
#room_u_state = 0
#
#room_d = room_choice(background)
#room_d_state = 0
#
#room_uu = room_choice(background)
#room_uu_state = 0
#
#room_uuu = room_choice(background)
#room_uuu_state = 0

hearts = pygame.image.load("assets/tiles/heart.png").convert()
hearts.set_colorkey((255, 255, 255))

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
            arrows.add(
                Arrow(sentry.rect.centerx, sentry.rect.centery, player.rect.centerx, player.rect.centery))

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