import pygame
import os
from const import *

class Reward(pygame.sprite.Sprite):

    school_list = []
    school_name = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        directory = os.fsencode("textures/assos")

        self.select_done = False
        self.selected_image = 0
        self.number_of_line = 5
        self.image_size = SCREEN_WIDTH / 6

        self.background = pygame.image.load('textures/background/bg_menu.png')
        self.background = pygame.transform.scale(self.background, (1080, 1000))

    def render(self, screen):
        screen.blit(self.background,(0,120))

    def reset(self):
        self.selected_image = 0
        self.select_done = False
