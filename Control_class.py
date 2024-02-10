import pygame
from pygame.locals import *

class Control():
    def __init__(self, joystick):
        self.joystick = joystick

    def left(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_LEFT] or self.joystick != None and self.joystick.get_axis(0) < -0.5

    def right(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_RIGHT] or self.joystick != None and self.joystick.get_axis(0) > 0.5

    def up(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_UP] or self.joystick != None and self.joystick.get_axis(1) < -0.5

    def down(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_DOWN] or self.joystick != None and self.joystick.get_axis(1) > 0.5

    def shoot(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_SPACE] or self.joystick != None and self.joystick.get_button(0)

    def escape(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_ESCAPE]



