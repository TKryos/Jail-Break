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



def room_rruuull2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_right(floor1)
    room_choice(floor1, room_data['room rruuull']['layout'], 0, player)
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
            floor_states['floor 5'] = 1

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


def room_rruuull1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_right(floor1)
    room_choice(floor1, room_data['room rruuull']['layout'], 0, player)
    item_choice(room_data['room rruuull']['item spawn'], floor1)
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

        # Code to check for hp_pots
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(max_hp_boosts) == 0 and len(atk_boosts) == 0 and len(rng_boosts) == 0 and
                    len(spd_boosts) == 0 and len(atk_spd_boosts) == 0 and len(knife_spd_boosts) == 0):
                room_data['room rruuull']['state'] = 2
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
            floor_states['floor 5'] = 1

            break

        if floor_states['floor 5'] == 1:
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
    if room_data['room rruuull']['state'] == 2:
        room_rruuull2(player, room_data, floor_states)


def room_rruuull0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_closed_boss_door_right(floor1)
    room_choice(floor1, room_data['room rruuull']['layout'], room_data['room rruuull']['final spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0 and len(arrows) == 0 and len(broken_prisoners) == 0:
                room_data['room rruuull']['state'] = 1
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
    room_rruuull1(player, room_data, floor_states)


def room_rruuulu1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_item_door_bot(floor1)
    room_choice(floor1, room_data['room rruuulu']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        if floor_states['floor 5'] == 1:
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


def room_rruuulu0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_item_door_bot(floor1)
    room_choice(floor1, room_data['room rruuulu']['layout'], 0, player)
    item_choice(room_data['room rruuulu']['item spawn'], floor1)
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

        # code to check if the item has been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(max_hp_boosts) == 0 and len(atk_boosts) == 0 and len(rng_boosts) == 0 and
                    len(spd_boosts) == 0 and len(atk_spd_boosts) == 0 and len(knife_spd_boosts) == 0):
                room_data['room rruuulu']['state'] = 1
                room = False

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rruuulu']['state'] == 1:
        room_rruuulu1(player, room_data, floor_states)


def room_rruuul2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_left(floor1)
    draw_open_item_door_top(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room rruuul']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room rruuull']['state'] == 0:
                room_rruuull0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuull']['state'] == 1:
                room_rruuull1(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuull']['state'] == 2:
                room_rruuull2(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruuulu']['state'] == 0:
                room_rruuulu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuulu']['state'] == 1:
                room_rruuulu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rruuul1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_2")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_left(floor1)
    draw_open_item_door_top(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room rruuul']['layout'], 0, player)
    if room_data['room rruuul']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rruuul']['pots'], floor1)
    else:
        pots2(room_data['room rruuul']['pots'], floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room rruuull']['state'] == 0:
                room_rruuull0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuull']['state'] == 1:
                room_rruuull1(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuull']['state'] == 2:
                room_rruuull2(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruuulu']['state'] == 0:
                room_rruuulu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

            elif room_data['room rruuulu']['state'] == 1:
                room_rruuulu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_open_boss_door_left(floor1)
                draw_open_item_door_top(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuul']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, right_doors, False):
            clear_objects()
            player.rect.center = SPRITE_LEFT

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rruuul']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rruuul']['state'] == 2:
        room_rruuul2(player, room_data, floor_states)


def room_rruuul0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_open_boss_door_left(floor1)
    draw_open_item_door_top(floor1)
    draw_right_open_door(floor1)
    room_choice(floor1, room_data['room rruuul']['layout'], room_data['room rruuul']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rruuul']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rruuul1(player, room_data, floor_states)


def room_rruuur2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    room_choice(floor1, room_data['room rruuur']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rruuur1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    room_choice(floor1, room_data['room rruuur']['layout'], 0, player)
    if room_data['room rruuur']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rruuur']['pots'], floor1)
    else:
        pots2(room_data['room rruuur']['pots'], floor1)
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
                room_data['room rruuur']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rruuur']['state'] == 2:
        room_rruuur2(player, room_data, floor_states)


def room_rruuur0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    room_choice(floor1, room_data['room rruuur']['layout'], room_data['room rruuur']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rruuur']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rruuur1(player, room_data, floor_states)


def room_rruuu2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rruuu']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room rruuul']['state'] == 0:
                room_rruuul0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuul']['state'] == 1:
                room_rruuul1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuul']['state'] == 2:
                room_rruuul2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rruuur']['state'] == 0:
                room_rruuur0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuur']['state'] == 1:
                room_rruuur1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuur']['state'] == 2:
                room_rruuur2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rruuu1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rruuu']['layout'], 0, player)
    if room_data['room rruuu']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rruuu']['pots'], floor1)
    else:
        pots2(room_data['room rruuu']['pots'], floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, left_doors, False):
            player.rect.center = SPRITE_RIGHT
            if room_data['room rruuul']['state'] == 0:
                room_rruuul0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_right_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuul']['state'] == 1:
                room_rruuul1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuul']['state'] == 2:
                room_rruuul2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, right_doors, False):
            player.rect.center = SPRITE_LEFT
            if room_data['room rruuur']['state'] == 0:
                room_rruuur0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuur']['state'] == 1:
                room_rruuur1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

            elif room_data['room rruuur']['state'] == 2:
                room_rruuur2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_bot_open_door(floor1)
                draw_right_open_door(floor1)
                room_choice(floor1, room_data['room rruuu']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rruuu']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rruuu']['state'] == 2:
        room_rruuu2(player, room_data, floor_states)


def room_rruuu0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_right_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rruuu']['layout'], room_data['room rruuu']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rruuu']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rruuu1(player, room_data, floor_states)


def room_rruu2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rruu']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruuu']['state'] == 0:
                room_rruuu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

            elif room_data['room rruuu']['state'] == 1:
                room_rruuu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

            elif room_data['room rruuu']['state'] == 2:
                room_rruuu2(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rruu1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rruu']['layout'], 0, player)
    if room_data['room rruu']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rruu']['pots'], floor1)
    else:
        pots2(room_data['room rruu']['pots'], floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruuu']['state'] == 0:
                room_rruuu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

            elif room_data['room rruuu']['state'] == 1:
                room_rruuu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

            elif room_data['room rruuu']['state'] == 2:
                room_rruuu2(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rruu']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rruu']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rruu']['state'] == 2:
        room_rruu2(player, room_data, floor_states)


def room_rruu0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_closed_door(floor1)
    draw_bot_closed_door(floor1)
    room_choice(floor1, room_data['room rruu']['layout'], room_data['room rruu']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rruu']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rruu1(player, room_data, floor_states)


def room_rrdd2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room rrdd']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rrdd1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room rrdd']['layout'], 0, player)
    if room_data['room rrdd']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rrdd']['pots'], floor1)
    else:
        pots2(room_data['room rrdd']['pots'], floor1)
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
                room_data['room rrdd']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rrdd']['state'] == 2:
        room_rrdd2(player, room_data, floor_states)


def room_rrdd0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_closed_door(floor1)
    room_choice(floor1, room_data['room rrdd']['layout'], room_data['room rrdd']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rrdd']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rrdd1(player, room_data, floor_states)


def room_rru2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rru']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruu']['state'] == 0:
                room_rruu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

            elif room_data['room rruu']['state'] == 1:
                room_rruu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

            elif room_data['room rruu']['state'] == 2:
                room_rruu2(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rru1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
    room_choice(floor1, room_data['room rru']['layout'], 0, player)
    if room_data['room rru']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rru']['pots'], floor1)
    else:
        pots2(room_data['room rru']['pots'], floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rruu']['state'] == 0:
                room_rruu0(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

            elif room_data['room rruu']['state'] == 1:
                room_rruu1(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

            elif room_data['room rruu']['state'] == 2:
                room_rruu2(player, room_data, floor_states)

                # For if you come back into the room
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rru']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, bot_doors, False):
            clear_objects()
            player.rect.center = SPRITE_TOP

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rru']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rru']['state'] == 2:
        room_rru2(player, room_data, floor_states)


def room_rru0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_top_closed_door(floor1)
    draw_bot_closed_door(floor1)
    room_choice(floor1, room_data['room rru']['layout'], room_data['room rru']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rru']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rru1(player, room_data, floor_states)


def room_rrd2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_open_door(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room rrd']['layout'], 0, player)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room rrdd']['state'] == 0:
                room_rrdd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

            elif room_data['room rrdd']['state'] == 1:
                room_rrdd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

            elif room_data['room rrdd']['state'] == 2:
                room_rrdd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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


def room_rrd1(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_open_door(floor1)
    draw_top_open_door(floor1)
    room_choice(floor1, room_data['room rrd']['layout'], 0, player)
    if room_data['room rrd']['layout'] == (0 or 3 or 4):
        pots1(room_data['room rrd']['pots'], floor1)
    else:
        pots2(room_data['room rrd']['pots'], floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room rrdd']['state'] == 0:
                room_rrdd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

            elif room_data['room rrdd']['state'] == 1:
                room_rrdd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

            elif room_data['room rrdd']['state'] == 2:
                room_rrdd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_bot_open_door(floor1)
                draw_top_open_door(floor1)
                room_choice(floor1, room_data['room rrd']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, top_doors, False):
            clear_objects()
            player.rect.center = SPRITE_BOTTOM

            # Returns to previous room
            break

        # code to check if all hp pots have been taken
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if len(hp_pots) == 0:
                room_data['room rrd']['state'] = 2
                room = False

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    if room_data['room rrd']['state'] == 2:
        room_rrd2(player, room_data, floor_states)


def room_rrd0(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_3")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_bot_closed_door(floor1)
    draw_top_closed_door(floor1)
    room_choice(floor1, room_data['room rrd']['layout'], room_data['room rrd']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rrd']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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
    room_rrd1(player, room_data, floor_states)


def room_rr2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rru']['state'] == 0:
                room_rru0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rru']['state'] == 1:
                room_rru1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rru']['state'] == 2:
                room_rru2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room rrd']['state'] == 0:
                room_rrd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrd']['state'] == 1:
                room_rrd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrd']['state'] == 2:
                room_rrd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

        elif pygame.sprite.spritecollide(player, left_doors, False):
            clear_objects()
            player.rect.center = SPRITE_RIGHT

            # Returns to previous room
            break

        # goes back to the beginning if the floor state is 1
        if floor_states['floor 5'] == 1:
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
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_open_door(floor1)
    draw_top_open_door(floor1)
    draw_bot_open_door(floor1)
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

        # Door interactions
        if pygame.sprite.spritecollide(player, top_doors, False):
            player.rect.center = SPRITE_BOTTOM
            if room_data['room rru']['state'] == 0:
                room_rru0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rru']['state'] == 1:
                room_rru1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rru']['state'] == 2:
                room_rru2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

        if pygame.sprite.spritecollide(player, bot_doors, False):
            player.rect.center = SPRITE_TOP
            if room_data['room rrd']['state'] == 0:
                room_rrd0(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrd']['state'] == 1:
                room_rrd1(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
                room_choice(floor1, room_data['room rr']['layout'], 0, player)

            elif room_data['room rrd']['state'] == 2:
                room_rrd2(player, room_data, floor_states)

                # For if you come back into the room
                draw_left_open_door(floor1)
                draw_top_open_door(floor1)
                draw_bot_open_door(floor1)
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
        if floor_states['floor 5'] == 1:
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
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    draw_top_closed_door(floor1)
    draw_bot_closed_door(floor1)
    room_choice(floor1, room_data['room rr']['layout'], room_data['room rr']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room rr']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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


def room_r2(player, room_data, floor_states):
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    floor1 = screen.copy()
    pygame.display.set_caption("Floor_5")

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
        if floor_states['floor 5'] == 1:
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
    pygame.display.set_caption("Floor_5")

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
        if floor_states['floor 5'] == 1:
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
    pygame.display.set_caption("Floor_5")

    # Reset the room objects
    clear_objects()

    draw_background(floor1)
    draw_left_closed_door(floor1)
    draw_right_closed_door(floor1)
    room_choice(floor1, room_data['room r']['layout'], room_data['room r']['enemy spawn'], player)
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

        # code to check if all enemies have been killed
        current_time = pygame.time.get_ticks()
        if current_time - TIME_SINCE_DOOR > 500:
            if (len(guards) == 0 and len(patrols) == 0 and len(sentries) == 0
                    and len(arrows) == 0 and len(broken_prisoners) == 0):
                room_data['room r']['state'] = 1
                room = False

        if floor_states['floor 5'] == 1:
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

