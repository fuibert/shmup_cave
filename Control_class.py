import pygame
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP

SENSIBILITY = 0.1

class Control():
    def __init__(self, joystick):
        self.joystick = joystick

    def left(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_LEFT] or self.joystick != None and self.joystick.get_axis(0) < -SENSIBILITY

    def right(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_RIGHT] or self.joystick != None and self.joystick.get_axis(0) > SENSIBILITY

    def up(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_UP] or self.joystick != None and self.joystick.get_axis(1) < -SENSIBILITY

    def down(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_DOWN] or self.joystick != None and self.joystick.get_axis(1) > SENSIBILITY

    def shoot(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_SPACE] or self.joystick != None and self.joystick.get_button(0)

    def escape(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_ESCAPE]

    def direction(self):
        if self.joystick != None:
            return (self.joystick.get_axis(0), self.joystick.get_axis(1)) 

        pressed_keys = pygame.key.get_pressed()
        dir_ = [0,0]
        if pressed_keys[K_LEFT]:
            dir_[0] -= 1  
        if pressed_keys[K_RIGHT]:
            dir_[0] += 1  
        if pressed_keys[K_UP]:
            dir_[1] -= 1  
        if pressed_keys[K_DOWN]:
            dir_[1] += 1  
        return dir_                      