import pygame
from pygame.locals import *
from const import *

class Player():
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("textures/Plane5.png")
        self.surf = pygame.Surface((52, 52))
        self.rect = self.surf.get_rect(center = (160, 520))
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

    def render(self, screen):
         screen.blit(self.image, self.rect)

    def update(self):
        self.move()
