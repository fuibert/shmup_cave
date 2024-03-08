import pygame
import os
from const import *

class Menu(pygame.sprite.Sprite):

    school_list = []
    school_name = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        directory = os.fsencode("textures/assos")

        self.select_done = False
        self.selected_image = 0
        self.number_of_line = 5
        self.image_size = SCREEN_WIDTH / 6

        self.background = pygame.image.load('textures/background/bg_menu.jpg')
        self.background = pygame.transform.scale(self.background, (1080, 1000))

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            image = pygame.image.load('textures/assos/' + filename)
            image = pygame.transform.scale(image, (self.image_size, self.image_size))
            Menu.school_list.append(image)
            Menu.school_name.append(filename.split(".")[0])



    def render(self, screen):
        if not self.select_done:
            compt = 0
            screen.blit(self.background,(0,350))
            for image in Menu.school_list:
                if compt == self.selected_image:
                    pygame.draw.circle(screen, (255, 255, 255, 255), (50 + self.image_size/2 + compt % self.number_of_line * self.image_size + 25, 500 + self.image_size/2 + compt // self.number_of_line * self.image_size), self.image_size/2+5)
                screen.blit(image, (50 + compt % self.number_of_line * self.image_size + 25, 500 + compt // self.number_of_line * self.image_size))
                compt += 1


    def chose_school(self, action):
        if action == "SHOOT":
            self.select_done = True
            return Menu.school_name[self.selected_image]
        if action == "DOWN" and self.selected_image + self.number_of_line < len(Menu.school_list):
            self.selected_image += self.number_of_line
        if action == "UP" and self.selected_image - self.number_of_line >= 0:
            self.selected_image -= self.number_of_line
        if action == "LEFT" and self.selected_image - 1 >= 0:
            self.selected_image -= 1
        if action == "RIGHT" and self.selected_image + 1 < len(Menu.school_list):
            self.selected_image += 1
        return

    def reset(self):
        self.selected_image = 0
        self.select_done = False
