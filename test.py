import pygame
import sys
import random
from game_parameters import *
from player import Knife, Player, knives
from enemy import enemies, sentries, patrols, guards, broken_prisoners, arrows, Arrow

def interactions(player):
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