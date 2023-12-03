import pygame
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_room0, draw_room1, draw_room2, draw_room3,
                   draw_room4, draw_room5, room_choice, r1_e1, r1_e2, r1_e3, r1_e4)
from door_layouts import draw_top_open_door, draw_open_item_door_bot
from player import knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash,
                     door_bot, door_top, door_left, door_right,
                     top_doors, left_doors, right_doors, bot_doors, clear_objects)
from items import (HealthPot, hp_pots,
                   SpdUp, spd_boosts, AtkSpdUp, atk_spd_boosts, KnifeSpdUp, knife_spd_boosts,
                   MaxHpUp, max_hp_boosts, AtkUp, atk_boosts, RngUp, rng_boosts, items)
import f1_rooms
from background import draw_background
import random


def main(player, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_1")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_f1_start_room(floor1)
    draw_top_open_door(floor1)
    draw_open_item_door_bot(floor1)

    clock = pygame.time.Clock()
    # set room states, layout, and enemies
    room_data = {'room s': {'state': 0, 'layout': 0},  # starting room
                 'room u': {'state': 0, 'layout': 0,
                            'enemy spawn': 0, 'pots': 0},
                 'room d': {'state': 0, 'layout': 0, 'item spawn': 0},  # Item room

                 'room uu': {'state': 0, 'layout': 0,
                             'enemy spawn': 0, 'pots': 1},
                 'room uuu': {'state': 0, 'layout': 0, 'enemy spawn': 0,
                              'item spawn': 0}}  # Final room

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

    LAST_THROW_TIME = 0
    LAST_DMG_TIME = 0

    floor = True
    while floor and player.hp > 0:
        for event in pygame.event.get():

            # This is all code that is going into every floor/room
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # This is for throwing knives
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                knife = Knife(player.rect.centerx, player.rect.centery, *event.pos, player.rng, player.knife_spd)

                # Code to limit how often you can throw knives
                current_time = pygame.time.get_ticks()
                if current_time - LAST_THROW_TIME >= player.atk_spd:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_throw.mp3"))
                    knives.add(knife)
                    LAST_THROW_TIME = current_time
        # Code to randomly decide when a sentry fires an arrow
        for sentry in sentries:

            chance = random.randint(0, 60)
            if chance == 1:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/arrow_throw.mp3"))
                arrows.add(Arrow(sentry.rect.centerx, sentry.rect.centery, player.rect.centerx, player.rect.centery))

        # Code to check for damage from different enemies and limit how often you can take damage
        if pygame.sprite.spritecollide(player, guards, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= GUARD_ATK
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= PAT_ATK
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= SENTRY_ATK
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= BP_ATK
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= ARROW_ATK
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))
            pygame.sprite.spritecollide(barrier, knives, True)
            pygame.sprite.spritecollide(barrier, arrows, True)

        # Code that checks if hp pots are grabbed
        if player.maxhp > player.hp:
            if pygame.sprite.spritecollide(player, hp_pots, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/drink_potion.wav"))
                player.health_potion(1)

        if pygame.sprite.spritecollide(player, spd_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.spd_up(2)

        if pygame.sprite.spritecollide(player, atk_spd_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.atk_spd_up(100)

        if pygame.sprite.spritecollide(player, knife_spd_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.knife_spd_up(1)

        if pygame.sprite.spritecollide(player, max_hp_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.max_hp_up(1)

        if pygame.sprite.spritecollide(player, atk_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.atk_up(5)

        if pygame.sprite.spritecollide(player, rng_boosts, True):
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/item_pickup.wav"))
            player.atk_rng_up(1)

        # Code that checks if enemies collide with knives and deals damage to them
        for group in enemies:
            for enemy in group:
                if pygame.sprite.spritecollide(enemy, knives, True):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                    enemy.hp -= player.atk
                    # If enemy hp drops to or below 0, it kills the sprite
                    if enemy.hp <= 0:
                        enemy.kill()
        LIVES = player.hp
        # This is all code that is going into every floor/room

        # Code to tell what door you are entering
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
            if room_data['room u']['state'] == 0:
                print('c to u')
                f1_rooms.room_u0(player, room_data, floor_states)

                # For if you come back into the room
                clear_objects()

                draw_top_open_door(floor1)
                draw_open_item_door_bot(floor1)

                draw_f1_start_room(floor1)

            elif room_data['room u']['state'] == 1:
                print('c to u cleared')
                f1_rooms.room_u1(player, room_data, floor_states)

                # For if you come back into the room
                clear_objects()

                draw_top_open_door(floor1)
                draw_open_item_door_bot(floor1)

                draw_f1_start_room(floor1)

            elif room_data['room u']['state'] == 2:
                print('c to u no pots')
                f1_rooms.room_u2(player, room_data, floor_states)

                # For if you come back into the room
                clear_objects()
                draw_top_open_door(floor1)
                draw_open_item_door_bot(floor1)
                draw_f1_start_room(floor1)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
            if room_data['room d']['state'] == 0:
                print('c to d')
                f1_rooms.room_d0(player, room_data, floor_states)

                # For if you come back into the room
                clear_objects()

                draw_top_open_door(floor1)
                draw_open_item_door_bot(floor1)

                draw_f1_start_room(floor1)

            elif room_data['room d']['state'] == 1:
                print('c to d cleared')
                f1_rooms.room_d1(player, room_data, floor_states)

                # For if you come back into the room
                clear_objects()
                # draw the doors of the previous room
                draw_top_open_door(floor1)
                draw_open_item_door_bot(floor1)
                # draw the previous room
                draw_f1_start_room(floor1)

        if floor_states['floor 1'] == 1:
            break

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