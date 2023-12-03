import pygame
import random
import math
import sys
from game_parameters import *
from rooms import (draw_f1_start_room, draw_room0, draw_room1, draw_room2, draw_room3,
                   draw_room4, draw_room5, draw_room6, room_choice, r1_e1, r1_e2, r1_e3, r1_e4)
from door_layouts import (draw_closed_doors, draw_top_closed_door, draw_bot_closed_door, draw_left_closed_door, draw_right_closed_door,
                          draw_open_doors, draw_top_open_door, draw_bot_open_door, draw_left_open_door, draw_right_open_door,
                          draw_closed_boss_door_top, draw_closed_boss_door_bot, draw_closed_boss_door_left, draw_closed_boss_door_right,
                          draw_open_boss_door_top, draw_open_boss_door_bot, draw_open_boss_door_left, draw_open_boss_door_right,
                          draw_closed_item_door_top, draw_closed_item_door_bot, draw_closed_item_door_left, draw_closed_item_door_right,
                          draw_open_item_door_top, draw_open_item_door_bot, draw_open_item_door_left, draw_open_item_door_right)
from background import draw_background
from player import Player, Knife, knives
from enemy import (Guard, Sentry, Patrol, Broken_Prisoner,
                   guards, sentries, patrols, broken_prisoners, Arrow, arrows, enemies)
from objects import (barriers, Barrier, floor_gashes, FloorGash)
from items import (HealthPot, hp_pots, pots1, pots2,
                   SpdUp, spd_boosts, AtkSpdUp, atk_spd_boosts, KnifeSpdUp, knife_spd_boosts,
                   MaxHpUp, max_hp_boosts, AtkUp, atk_boosts, RngUp, rng_boosts, items)


#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()

#overall background
draw_background(background)

draw_room6(background)
draw_closed_boss_door_bot(background)
draw_closed_boss_door_right(background)
#room_choice(background)

#create the player
player = Player(JAIL_X_END - TILE_SIZE // 2, SCREEN_HEIGHT/2)

hearts = pygame.image.load("assets/tiles/heart.png").convert()
hearts.set_colorkey((255,255,255))

pots1(1, background)
pots1(0, background)
pots2(0, background)
pots2(1, background)

#hp_pots.add(HealthPot(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE*2))
#spd_boosts.add(SpdUp(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*2))
#atk_spd_boosts.add(AtkSpdUp(JAIL_X_START + TILE_SIZE*6, JAIL_Y_START + TILE_SIZE*2))
#knife_spd_boosts.add(KnifeSpdUp(JAIL_X_START + TILE_SIZE*8, JAIL_Y_START + TILE_SIZE*2))
#max_hp_boosts.add(MaxHpUp(JAIL_X_START + TILE_SIZE*10, JAIL_Y_START + TILE_SIZE*2))
#atk_boosts.add(AtkUp(JAIL_X_START + TILE_SIZE*2, JAIL_Y_START + TILE_SIZE*4))
#rng_boosts.add(RngUp(JAIL_X_START + TILE_SIZE*4, JAIL_Y_START + TILE_SIZE*4))

#create the enemies
#r1_e3()
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
            knife = Knife(player.rect.centerx, player.rect.centery, *event.pos, player.rng, player.knife_spd)

        ####code to limit how often you can throw knives
            current_time = pygame.time.get_ticks()
            if current_time - LAST_THROW_TIME >= player.atk_spd:
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_throw.mp3"))
                knives.add(knife)
                LAST_THROW_TIME = current_time
####code to randomly decide when a sentry fires an arrow
    for sentry in sentries:

        chance = random.randint(0, 60)
        if chance == 1:
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/arrow_throw.mp3"))
            arrows.add(Arrow(sentry.rect.centerx, sentry.rect.centery, player.rect.centerx, player.rect.centery))

####code to check for damage from different enemies and limit how often you can take damage
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

####Code that checks if enemies collide with knives and deals damage to them
    for group in enemies:
        for enemy in group:
            if pygame.sprite.spritecollide(enemy, knives, True):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/tiles/knife_in_flesh.mp3"))
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
    hp_pots.draw(screen)
    for item in items:
        item.draw(screen)

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
    #update the display
    pygame.display.flip()

    #limit the fps
    clock.tick(30)

#quit pygame
pygame.quit()
sys.exit()