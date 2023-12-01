import pygame
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_open_doors, draw_closed_doors,
                   draw_room0, draw_room1, draw_room2, draw_room3, draw_room4, draw_room5,
                   room_choice, r1_e1, r1_e2, r1_e3, r1_e4)
from player import knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash,
                     door_bot, door_top, door_left, door_right, top_doors, left_doors, right_doors, bot_doors)
import f1_rooms
from background import draw_background
import random


def main(player):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_1")

    draw_background(floor1)
    draw_room0(floor1)

    clock = pygame.time.Clock()
    # Make the possible rooms and their states
    room_c = draw_f1_start_room(floor1)
    room_c_state = 1
    draw_open_doors(floor1)

    room_l, enemy_l = random.randint(0, 6), random.randint(0, 4)
    room_l_state = 0

    room_r, enemy_r = random.randint(0, 6), random.randint(0, 4)
    room_r_state = 0

    room_u, enemy_u = 1, 1 #random.randint(0, 6), random.randint(0, 4)
    enemies_u = random.randint(0, 4)
    room_u_state = [0]

    room_d, enemy_d = random.randint(0, 6), random.randint(0, 4)
    room_d_state = 0

    room_uu, enemy_u = random.randint(0, 6), random.randint(0, 4)
    room_uu_state = 0

    room_uuu = 0
    room_uuu_state = 0

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((255, 255, 255))

    LAST_THROW_TIME = 0
    LAST_DMG_TIME = 0

    floor = True
    while floor and player.hp > 0:

        # This is code that goes into ever floor/room
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # This is for throwing knives

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                knife = Knife(player.rect.centerx, player.rect.centery, *event.pos, player.rng)

                # Code to limit how often you can throw knives
                current_time = pygame.time.get_ticks()
                if current_time - LAST_THROW_TIME >= player.atk_spd:
                    knives.add(knife)
                    LAST_THROW_TIME = current_time
        # Code to randomly decide when a sentry fires an arrow
        for sentry in sentries:

            chance = random.randint(0, 60)
            if chance == 1:
                arrows.add(
                    Arrow(sentry.rect.centerx, sentry.rect.centery, player.rect.centerx, player.rect.centery))

        # Code to check for damage from different enemies and limit how often you can take damage
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

        # Code that checks if enemies collide with knives and deals damage to them
        for group in enemies:
            for enemy in group:
                if pygame.sprite.spritecollide(enemy, knives, True):
                    enemy.hp -= player.atk
                    # If enemy hp drops to or below 0, it kills the sprite
                    if enemy.hp <= 0:
                        enemy.kill()
        LIVES = player.hp
        # This is all code that is going into every floor/room

        # Code to tell what door you are entering
        if pygame.sprite.spritecollide(player, top_doors, False):
            print('going up')
            if room_u_state[0] == 0:
                player.rect.center = (SCREEN_WIDTH//2, JAIL_Y_END - TILE_SIZE/2)
                f1_rooms.room_u0(player, room_u_state, room_u, enemy_u)
            if room_u_state == 1:
                player.rect.center = (SCREEN_WIDTH//2, JAIL_Y_END - TILE_SIZE/2)
                f1_rooms.room_u1(player, room_u)
                draw_room0(floor1)
        if pygame.sprite.spritecollide(player, right_doors, False):
            print('right way')

        if pygame.sprite.spritecollide(player, left_doors, False):
            print('left here')

        if pygame.sprite.spritecollide(player, bot_doors, False):
            print('long way down')



        # Draw background
        screen.blit(floor1, (0,0))

        # Update player location
        player.update(barriers, floor_gashes)
        guards.update(barriers, floor_gashes)
        patrols.update(barriers, floor_gashes)
        broken_prisoners.update(barriers, floor_gashes)
        arrows.update()
        knives.update(barriers)

        # Draw game objects
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        arrows.draw(screen)
        knives.draw(screen)

        for i in range(player.hp):
            if i <= 9:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-1), JAIL_Y_END + TILE_SIZE))
            elif i <= 19:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-11), JAIL_Y_END + TILE_SIZE*2))
            elif i <= 29:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE*(i-21), JAIL_Y_END + TILE_SIZE*3))
        # Update the display
        pygame.display.flip()

        # Limit the fps
        clock.tick(30)