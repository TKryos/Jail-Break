#"""Code for doors of the item room"""
#if pygame.sprite.spritecollide(player, top_doors, False):
#    print('d to c')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#
#    # Returns to previous room
#    break
#
#
#"""Code for the doors of the boss room"""
#"""Code for state 2 of the boss room"""
## Outer to Inner
#if pygame.sprite.spritecollide(player, bot_doors, False):
#    print('uuu to uu')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#
#    # Returns to previous room
#    break
#
## Stairs to the next floor
#if pygame.sprite.spritecollide(player, stairs, False):
#    print('next floor')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
#    floor_states['floor 1'] = 1
#
#    break
#
#"""Code for state 1 of the boss room"""
## Inner to Outer uu to uuu
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    print('uu to uuu')
#
## Outer to Inner
#elif pygame.sprite.spritecollide(player, bot_doors, False):
#    print('uu to u')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#
#    # Returns to previous room
#    break
#
## Stairs to the next floor
#if pygame.sprite.spritecollide(player, stairs, False):
#    print('next floor')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
#    floor_states['floor 1'] = 1
#
#    break
#
#
#"""Code for normal enemy rooms"""
#"""Code for state 2 of normal enemy rooms"""
## Code to tell what door you are entering
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    if room_data['room uu']['state'] == 0:
#        print('u to uu')
#        room_uu0(player, room_data, floor_states)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#    elif room_data['room uu']['state'] == 1:
#        print('u to uu cleared')
#        room_uu1(player, room_data, floor_states)
#
#        # For if you come back into th eroom
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#    elif room_data['room uu']['state'] == 2:
#        room_uu2(player, room_data, floor_states)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#elif pygame.sprite.spritecollide(player, bot_doors, False):
#    print('u to c')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#
#    # Returns to previous room
#    break
#
#"""Code for state 1 of normal enemy rooms"""
## Code to tell what door you are entering
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    if room_data['room uu']['state'] == 0:
#        print('u to uu')
#        room_uu0(player, room_data, floor_states)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#    elif room_data['room uu']['state'] == 1:
#        print('u to uu cleared')
#        room_uu1(player, room_data, floor_states)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#    elif room_data['room uu']['states'] == 2:
#        room_uu2(player, room_data, floor_states)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)
#        draw_bot_open_door(floor1)
#        room_choice(floor1, room_data['room u']['layout'], 0, player)
#
#elif pygame.sprite.spritecollide(player, bot_doors, False):
#    print('u to c')
#    clear_objects()
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#    print('here')
#    # Returns to previous room
#    break
#
#"""Code for the starting room"""
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    if room_data['room u']['state'] == 0:
#        print('c to u')
#        f1_rooms.room_u0(player, room_data, floor_states)
#
#        # For if you come back into the room
#        clear_objects()
#
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#
#        draw_f1_start_room(floor1)
#
#    elif room_data['room u']['state'] == 1:
#        print('c to u cleared')
#        f1_rooms.room_u1(player, room_data, floor_states)
#
#        # For if you come back into the room
#        clear_objects()
#
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#
#        draw_f1_start_room(floor1)
#
#    elif room_data['room u']['state'] == 2:
#        print('c to u no pots')
#        f1_rooms.room_u2(player, room_data, floor_states)
#
#        # For if you come back into the room
#        clear_objects()
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#        draw_f1_start_room(floor1)
#
#elif pygame.sprite.spritecollide(player, bot_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#    if room_data['room d']['state'] == 0:
#        print('c to d')
#        f1_rooms.room_d0(player, room_data, floor_states)
#
#        # For if you come back into the room
#        clear_objects()
#
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#
#        draw_f1_start_room(floor1)
#
#    elif room_data['room d']['state'] == 1:
#        print('c to d cleared')
#        f1_rooms.room_d1(player, room_data, floor_states)
#
#        # For if you come back into the room
#        clear_objects()
#        # draw the doors of the previous room
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#        # draw the previous room
#        draw_f1_start_room(floor1)