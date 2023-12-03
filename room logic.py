"""Code for going from first room to outer room"""
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    if room_data['room u']['state'] == 0:
#        print('c to u')
#        f1_rooms.room_u0(player, room_data)
#
#        # For if you come back into the room
#        clear_objects()
#        draw_f1_start_room(floor1)
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)
#
#    elif room_data['room u']['state'] == 1:
#        print('c to u cleared')
#        f1_rooms.room_u1(player, room_data)
#
#        # For if you come back into the room
#        clear_objects()
#        draw_f1_start_room(floor1)
#        draw_top_open_door(floor1)
#        draw_open_item_door_bot(floor1)


"""Code for going from inner room to outer room"""
#if pygame.sprite.spritecollide(player, top_doors, False):
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_END - TILE_SIZE / 2)
#    if room_data['room uu']['state'] == 0:
#        print('u to uu')
#        room_uu0(player, room_data)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)                                             # doors based on overall floor layout
#        draw_bot_open_door(floor1)                                             # doors based on overall floor layout
#        room_choice(floor1, room_data['room u']['layout'], 0, player)          # rooms drawn based on room data
#
#    elif room_data['room uu']['state'] == 1:
#        print('u to uu cleared')
#        room_uu1(player, room_data)
#
#        # For if you come back into the room
#        draw_top_open_door(floor1)                                             # doors based on overall floor layout
#        draw_bot_open_door(floor1)                                             # doors based on overall floor layout
#        room_choice(floor1, room_data['room u']['layout'], 0, player)          # rooms drawn based on room data
#
"""Code for going from outer room to inner room"""
#if pygame.sprite.spritecollide(player, bot_doors, False):
#    print('u to c')
#    clear_objects()                                                            # clears barriers and holes
#    player.rect.center = (SCREEN_WIDTH // 2, JAIL_Y_START + TILE_SIZE / 2)
#
#    # Returns to previous room
#    break