#from test1 import func2
#
#def func1():
#    dict1 = {'room' :
#                 {'state' : 0,
#                  'layout' : 1,
#                  'enemy spawn' : 1}}
#    func2(dict1)
#    print(dict1)
#
#func1()

import pygame
import msvcrt


def count_pressed_keys():
    while True:
        # Use msvcrt.kbhit() to check if a key is pressed
        num_pressed_keys = sum(1 for _ in range(256) if msvcrt.kbhit())

        # Print the result
        print(f"Number of keys pressed: {num_pressed_keys}")

        # Use a sleep to avoid high CPU usage
        msvcrt.getch()


count_pressed_keys()

