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