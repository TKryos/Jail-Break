import pygame
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_room0, draw_room1, draw_room2, draw_room3,
                   draw_room4, draw_room5, room_choice, r1_e1, r1_e2, r1_e3, r1_e4, )
from door_layouts import (draw_closed_doors, draw_top_closed_door, draw_bot_closed_door, draw_left_closed_door, draw_right_closed_door,
                          draw_open_doors, draw_top_open_door, draw_bot_open_door, draw_left_open_door, draw_right_open_door,
                          draw_closed_boss_door_top, draw_closed_boss_door_bot, draw_closed_boss_door_left, draw_closed_boss_door_right,
                          draw_open_boss_door_top, draw_open_boss_door_bot, draw_open_boss_door_left, draw_open_boss_door_right,
                          draw_closed_item_door_top, draw_closed_item_door_bot, draw_closed_item_door_left, draw_closed_item_door_right,
                          draw_open_item_door_top, draw_open_item_door_bot, draw_open_item_door_left, draw_open_item_door_right)
from player import knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash,
                     door_bot, door_top, door_left, door_right,
                     top_doors, left_doors, right_doors, bot_doors, clear_objects)
from background import draw_background
import random

def room_uu1(player, room_num):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_1")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_num, 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((255, 255, 255))

    LAST_THROW_TIME = 0
    LAST_DMG_TIME = 0

    room = True
    while room and player.hp > 0:
        for event in pygame.event.get():

            # This is all code that is going into every floor/room
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

            chance = random.randint(0, ARROW_CHANCE)
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
            print('room_u1')

            clear_objects()

        if pygame.sprite.spritecollide(player, right_doors, False):
            print('right way')

            clear_objects()

        if pygame.sprite.spritecollide(player, left_doors, False):
            print('left here')

            clear_objects()

        # Code to return to last room and go up one level in the while loop
        if pygame.sprite.spritecollide(player, bot_doors, False):
            print('long way down')
            player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
            clear_objects()

            break

        # Draw background
        screen.blit(floor1, (0, 0))

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
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 1), JAIL_Y_END + TILE_SIZE))
            elif i <= 19:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 11), JAIL_Y_END + TILE_SIZE * 2))
            elif i <= 29:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 21), JAIL_Y_END + TILE_SIZE * 3))
        # Update the display
        pygame.display.flip()

        # Limit the fps
        clock.tick(30)


def room_uu0(player, state, room_num, enemy_num):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_1")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_closed_door(floor1)
    draw_bot_closed_door(floor1)
    room_choice(floor1, room_num, enemy_num, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((255, 255, 255))

    LAST_THROW_TIME = 0
    LAST_DMG_TIME = 0

    room = True
    while room and player.hp > 0:
        for event in pygame.event.get():

            # This is all code that is going into every floor/room
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

            chance = random.randint(0, ARROW_CHANCE)
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

        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            pygame.sprite.spritecollide(barrier, knives, True)

        for barrier in barriers:
            pygame.sprite.spritecollide(barrier, arrows, True)

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0 and len(arrows) == 0 and len(
                    broken_prisoners) == 0:
                state[0] = 1
                room = False

        # Draw background
        screen.blit(floor1, (0, 0))

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
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 1), JAIL_Y_END + TILE_SIZE))
            elif i <= 19:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 11), JAIL_Y_END + TILE_SIZE * 2))
            elif i <= 29:
                screen.blit(hearts, (JAIL_X_START + TILE_SIZE * (i - 21), JAIL_Y_END + TILE_SIZE * 3))
        # Update the display
        pygame.display.flip()

        # Limit the fps
        clock.tick(30)
    # Outside of while loop call room_state1
    room_uu1(player, room_num)
