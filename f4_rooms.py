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
                          draw_open_item_door_top, draw_open_item_door_bot, draw_open_item_door_left, draw_open_item_door_right,
                          draw_stairs)
from player import knives, Knife
from enemy import (guards, patrols, sentries, arrows, Arrow, broken_prisoners, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash, stairs,
                     door_bot, door_top, door_left, door_right,
                     top_doors, left_doors, right_doors, bot_doors, clear_objects)
from items import (HealthPot, hp_pots, item_choice, pots1, pots2,
                   SpdUp, spd_boosts, AtkSpdUp, atk_spd_boosts, KnifeSpdUp, knife_spd_boosts,
                   MaxHpUp, max_hp_boosts, AtkUp, atk_boosts, RngUp, rng_boosts, items)
from background import draw_background
import random


def room_lll2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_right(floor1)
    room_choice(floor1, room_data['room lll']['layout'], 0, player)
    draw_stairs(floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # Stairs to the next floor
        if pygame.sprite.spritecollide(player, stairs, False):
            clear_objects()
            player.rect.center = SPRITE_MIDDLE
            floor_states['floor 4'] = 1

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


def room_lll1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_right(floor1)
    room_choice(floor1, room_data['room lll']['layout'], 0, player)
    item_choice(room_data['room lll']['item spawn'], floor1)
    draw_stairs(floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Code to check for hp_pots
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(max_hp_boosts) == 0 and len(atk_boosts) == 0 and len(rng_boosts) == 0 and
                    len(spd_boosts) == 0 and len(atk_spd_boosts) == 0 and len(knife_spd_boosts) == 0):
                room_data['room lll']['state'] = 2
                room = False

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # Stairs to the next floor
        if pygame.sprite.spritecollide(player, stairs, False):
            clear_objects()
            player.rect.center = SPRITE_MIDDLE
            floor_states['floor 4'] = 1

            break

        if floor_states['floor 4'] == 1:
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
    if room_data['room lll']['state'] == 2:
        room_lll2(player, room_data, floor_states)


def room_lll0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_closed_boss_door_right(floor1)
    room_choice(floor1, room_data['room lll']['layout'], room_data['room lll']['final spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0 and len(arrows) == 0 and len(broken_prisoners) == 0:
                room_data['room lll']['state'] = 1
                room = False

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
        hp_pots.draw(screen)

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
    # Outside of while loop call room_state1
    room_lll1(player, room_data, floor_states)


def room_rrr2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    room_choice(floor1, room_data['room rrr']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_rrr1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    room_choice(floor1, room_data['room rrr']['layout'], 0, player)
    if room_data['room rrr']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rrr']['pots'], floor1)
    else:
        pots2(room_data['room rrr']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rrr']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room rrr']['state'] == 2:
        room_rrr2(player, room_data, floor_states)


def room_rrr0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    room_choice(floor1, room_data['room rrr']['layout'], room_data['room rrr']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rrr']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_rrr1(player, room_data, floor_states)


def room_ll2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_left(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room ll']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room lll']['state'] == 0:
                room_lll0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

            elif room_data['room lll']['state'] == 1:
                room_lll1(player, room_data, floor_states)

                # For if you come back into th eroom
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

            elif room_data['room lll']['state'] == 2:
                room_lll2(player, room_data, floor_states)

                # For if you come back into th eroom
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_ll1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_left(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room ll']['layout'], 0, player)
    if room_data['room ll']['layout'] == (0 or 3 or 4):
        pots1(room_data['room ll']['pots'], floor1)
    else:
        pots2(room_data['room ll']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room lll']['state'] == 0:
                room_lll0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

            elif room_data['room lll']['state'] == 1:
                room_lll1(player, room_data, floor_states)

                # For if you come back into th eroom
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

            elif room_data['room lll']['state'] == 2:
                room_lll2(player, room_data, floor_states)

                # For if you come back into th eroom
                draw_open_boss_door_left(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room ll']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room ll']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room ll']['state'] == 2:
        room_ll2(player, room_data, floor_states)


def room_ll0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_closed_boss_door_left(floor1)
    draw_right_closed_door(floor1)
    room_choice(floor1, room_data['room ll']['layout'], room_data['room ll']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room ll']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_ll1(player, room_data, floor_states)


def room_dd2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room dd']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_dd1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room dd']['layout'], 0, player)
    if room_data['room dd']['layout'] == (0 or 3 or 4):
        pots1(room_data['room dd']['pots'], floor1)
    else:
        pots2(room_data['room dd']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room dd']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room dd']['state'] == 2:
        room_dd2(player, room_data, floor_states)


def room_dd0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_closed_door(floor1)
    room_choice(floor1, room_data['room dd']['layout'], room_data['room dd']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room dd']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_dd1(player, room_data, floor_states)


def room_rr2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room rr']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rrr']['state'] == 0:
                room_rrr0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrr']['state'] == 1:
                room_rrr1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrr']['state'] == 2:
                room_rrr2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_rr1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room rr']['layout'], 0, player)
    if room_data['room rr']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rr']['pots'], floor1)
    else:
        pots2(room_data['room rr']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rrr']['state'] == 0:
                room_rrr0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrr']['state'] == 1:
                room_rrr1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrr']['state'] == 2:
                room_rrr2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rr']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room rr']['state'] == 2:
        room_rr2(player, room_data, floor_states)


def room_rr0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    draw_right_closed_door(floor1)
    room_choice(floor1, room_data['room rr']['layout'], room_data['room rr']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rr']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_rr1(player, room_data, floor_states)


def room_l2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room l']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room ll']['state'] == 0:
                room_ll0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

            elif room_data['room ll']['state'] == 1:
                room_ll1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

            elif room_data['room ll']['state'] == 2:
                room_ll2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_l1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room l']['layout'], 0, player)
    if room_data['room l']['layout'] == (0 or 3 or 4):
        pots2(room_data['room l']['pots'], floor1)
    else:
        pots1(room_data['room l']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room ll']['state'] == 0:
                room_ll0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

            elif room_data['room ll']['state'] == 1:
                room_ll1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

            elif room_data['room ll']['state'] == 2:
                room_ll2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room l']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room l']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room l']['state'] == 2:
        room_l2(player, room_data, floor_states)


def room_l0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    draw_right_closed_door(floor1)
    room_choice(floor1, room_data['room l']['layout'], room_data['room l']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room l']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_l1(player, room_data, floor_states)


def room_d2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_open_door(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room d']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room dd']['state'] == 0:
                room_dd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

            elif room_data['room dd']['state'] == 1:
                room_dd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

            elif room_data['room dd']['state'] == 2:
                room_dd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_d1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_open_door(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room d']['layout'], 0, player)
    if room_data['room d']['layout'] == (0 or 3 or 4):
        pots1(room_data['room d']['pots'], floor1)
    else:
        pots2(room_data['room d']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room dd']['state'] == 0:
                room_dd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

            elif room_data['room dd']['state'] == 1:
                room_dd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

            elif room_data['room dd']['state'] == 2:
                room_dd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room d']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room d']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room d']['state'] == 2:
        room_d2(player, room_data, floor_states)


def room_d0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_closed_door(floor1)
    draw_top_closed_door(floor1)
    room_choice(floor1, room_data['room d']['layout'], room_data['room d']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room d']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_d1(player, room_data, floor_states)


def room_r2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room r']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rr']['state'] == 0:
                room_rr0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

            elif room_data['room rr']['state'] == 1:
                room_rr1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

            elif room_data['room rr']['state'] == 2:
                room_rr2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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


def room_r1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room r']['layout'], 0, player)
    if room_data['room r']['layout'] == (0 or 3 or 4):
        pots1(room_data['room r']['pots'], floor1)
    else:
        pots2(room_data['room r']['pots'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rr']['state'] == 0:
                room_rr0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

            elif room_data['room rr']['state'] == 1:
                room_rr1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

            elif room_data['room rr']['state'] == 2:
                room_rr2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room r']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room r']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room r']['state'] == 2:
        room_r2(player, room_data, floor_states)


def room_r0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    draw_right_closed_door(floor1)
    room_choice(floor1, room_data['room r']['layout'], room_data['room r']['enemy spawn'], player, 2)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room r']['state'] = 1
                room = False

        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    room_r1(player, room_data, floor_states)


def room_u1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_item_door_bot(floor1)
    room_choice(floor1, room_data['room u']['layout'], 0, player)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        if floor_states['floor 4'] == 1:
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


def room_u0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_4")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_item_door_bot(floor1)
    room_choice(floor1, room_data['room u']['layout'], 0, player, 2)
    item_choice(room_data['room u']['item spawn'], floor1)
    clock = pygame.time.Clock()
    TIME_SINCE_DOOR = pygame.time.get_ticks()

    # Hearts and time stuff
    hearts = pygame.image.load("assets/tiles/heart.png").convert()
    hearts.set_colorkey((0, 0, 0))

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
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, patrols, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, sentries, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, broken_prisoners, False):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/hurt.wav"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time

        if pygame.sprite.spritecollide(player, arrows, True):
            current_time = pygame.time.get_ticks()
            if current_time - LAST_DMG_TIME >= 1000:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
                player.hp -= LVLDMG
                LAST_DMG_TIME = current_time
        # Code that checks if projectiles collide with barriers and kills them
        for barrier in barriers:
            if pygame.sprite.spritecollide(barrier, knives, True) or pygame.sprite.spritecollide(barrier, arrows, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_wall.mp3"))

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

        # code to check if the item has been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(max_hp_boosts) == 0 and len(atk_boosts) == 0 and len(rng_boosts) == 0 and
                    len(spd_boosts) == 0 and len(atk_spd_boosts) == 0 and len(knife_spd_boosts) == 0):
                room_data['room u']['state'] = 1
                room = False

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 4'] == 1:
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
        hp_pots.draw(screen)

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
    if room_data['room u']['state'] == 1:
        room_u1(player, room_data, floor_states)
