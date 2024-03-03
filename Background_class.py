import pygame
from pygame.locals import K_1,K_2,K_3,K_4,K_5
from const import *

class Background(pygame.sprite.WeakSprite):
    def __init__(self, width):
        pygame.sprite.Sprite.__init__(self)
        self.bgimage = pygame.image.load('textures/background/' + BACKGROUND_IMAGE)
        self.bgimage = pygame.transform.scale_by(self.bgimage, width/ self.bgimage.get_rect().width)
        self.rectBGimg = self.bgimage.get_rect()
        self.type = 0
 
        self.bgX = 0
        self.bgY1 = 0 
        self.bgY2 = -self.rectBGimg.height

        self.movingUpSpeed = -3 * 60 *5

        self.animated = False
         
    def update(self):
        if self.animated:
            self.bgY1 -= self.movingUpSpeed / FPS
            self.bgY2 -= self.movingUpSpeed / FPS
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

        self.bgX = 0
                     
    def render(self, screen):
        screen.blit(self.bgimage, (self.bgX, self.bgY1))
        screen.blit(self.bgimage, (self.bgX, self.bgY2))

    def animate(self, bool_):
        self.animated = bool_