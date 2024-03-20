from tkinter import Y
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
        self.number_of_column = 6
        self.margin = {"x" : 0.1, "y" : 0.15}            
        self.image_size = {"width" : SCREEN_WIDTH * (1 - 2 * self.margin["x"]) / self.number_of_column,
                           "height": SCREEN_WIDTH * (1 - 2 * self.margin["y"]) / self.number_of_column}

        self.background = pygame.image.load('textures/background/bg_menu.png')
        self.height = SCREEN_WIDTH * self.background.get_height() /self.background.get_width()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, self.height))

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            image = pygame.image.load('textures/assos/' + filename)
            image = pygame.transform.scale(image, list(self.image_size.values()))
            Menu.school_list.append(image)
            Menu.school_name.append(filename.split(".")[0])



    def render(self, screen):
        screen.blit(self.background,(0,SCREEN_HEIGHT * 0.15))
        pygame.draw.circle(screen, WHITE, self.calc_coord(self.selected_image, True), self.image_size["width"] * 0.6)
        for i in range(len(Menu.school_list)):
            image = Menu.school_list[i]
            screen.blit(image, self.calc_coord(i))

    def calc_coord(self, index, centered = False):
        x = self.background.get_width() * self.margin["x"] + (index % self.number_of_column) * self.image_size["width"]
        y = SCREEN_HEIGHT * 0.15 + self.height * self.margin["y"] + (index // self.number_of_column) * self.image_size["width"] 
        if centered:
            x += self.image_size["width"] * 0.5   
            y += self.image_size["width"] * 0.5                     
        return (x, y)              
                            


    def chose_school(self, action):
        if action == "SHOOT":
            self.select_done = True
            return Menu.school_name[self.selected_image]
        if action == "DOWN" and self.selected_image + self.number_of_column < len(Menu.school_list):
            self.selected_image += self.number_of_column
        if action == "UP" and self.selected_image - self.number_of_column >= 0:
            self.selected_image -= self.number_of_column
        if action == "LEFT" and self.selected_image - 1 >= 0:
            self.selected_image -= 1
        if action == "RIGHT" and self.selected_image + 1 < len(Menu.school_list):
            self.selected_image += 1
        return

    def reset(self):
        self.selected_image = 0
        self.select_done = False
