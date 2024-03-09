import pygame
import os
from const import *
import pandas

class Statistics(pygame.sprite.Sprite):
    def __init__(self):
        self.background = pygame.image.load('textures/background/bg_stat.jpg')
        self.background = pygame.transform.scale(self.background, (1080, 1000))

        self.font_score = pygame.font.Font("src/fonts/" + STAT_FONT, STAT_SIZE)
        self.top = {}

    def render(self, screen):
        ## top 10 general
        screen.blit(self.background, (0, 1000))
        # for ecole in self.top:


        ## top ecole
        nb_score = 0
        for school in self.top:
            score_tmp = self.font_score.render(str(school) + ": " + str(self.top[school]), True, BLACK)
            if nb_score % 2 == 0:
                place = 0.25
            else:
                place = 0.75
            screen.blit(score_tmp, ((SCREEN_WIDTH * place) - (score_tmp.get_rect().width / 2), 1150 + (nb_score // 2) * STAT_SIZE))
            nb_score += 1

    def reset(self, score_board):
        ## top 10
        # df = pandas.json_normalize(score_board)
        # for item, value in df.items():
        #     print(value)

        ## top ecole
        for school in score_board:
            if len(score_board[school]) > 0:
                self.top[school] = max(score_board[school])
            else:
                self.top[school] = 0