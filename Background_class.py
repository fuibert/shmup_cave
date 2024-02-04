import pygame
from pygame.locals import *
from const import *

class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('textures/bg_1440x960.png')
            self.rectBGimg = self.bgimage.get_rect()
            self.type = 1
 
            self.bgX = -self.rectBGimg.width * self.type / 5
            self.bgY1 = 0 
            self.bgY2 = -self.rectBGimg.height
 
            self.movingUpSpeed = -3
         
      def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_1]:
            self.type = 0
        elif pressed_keys[K_2]:
            self.type = 1
        elif pressed_keys[K_3]:
            self.type = 2
        elif pressed_keys[K_4]:
            self.type = 3
        elif pressed_keys[K_5]:
            self.type = 4

        self.bgX = -self.rectBGimg.width * self.type / 5
             
      def render(self, screen):
         screen.blit(self.bgimage, (self.bgX, self.bgY1))
         screen.blit(self.bgimage, (self.bgX, self.bgY2))


