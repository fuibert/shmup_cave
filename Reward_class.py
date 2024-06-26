import pygame
import os
from const import *

class Reward(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.background = pygame.image.load('textures/background/reward.png')
        self.height = SCREEN_WIDTH * self.background.get_height() / self.background.get_width()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, self.height))

    def render(self, screen):
        screen.blit(self.background,(0,120))

    def reset(self):
        pass
