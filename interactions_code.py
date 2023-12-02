# This is code that goes into ever floor/room
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # This is for throwing knives

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        knife = Knife(player.rect.centerx, player.rect.centery, *event.pos, player.rng, player.knife_spd)

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
    pygame.sprite.spritecollide(barrier, arrows, True)

# Code that checks if hp pots are grabbed
if player.maxhp > player.hp:
    if pygame.sprite.spritecollide(player, hp_pots, True):
        player.health_potion(1)

if pygame.sprite.spritecollide(player, spd_boosts, True):
    player.spd_up(2)

if pygame.sprite.spritecollide(player, atk_spd_boosts, True):
    player.atk_spd_up(100)

if pygame.sprite.spritecollide(player, knife_spd_boosts, True):
    player.knife_spd_up(1)

if pygame.sprite.spritecollide(player, max_hp_boosts, True):
    player.max_hp_up(1)

if pygame.sprite.spritecollide(player, atk_boosts, True):
    player.atk_up(5)

if pygame.sprite.spritecollide(player, rng_boosts, True):
    player.atk_rng_up(1)

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