import pygame
import os
from const import *

class Statistics(pygame.sprite.Sprite):
    def __init__(self):
        self.background = pygame.image.load('textures/background/bg_stat.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_WIDTH * self.background.get_height() / self.background.get_width()))

        self.font_score = pygame.font.Font("src/fonts/" + STAT_FONT, STAT_SIZE)
        self.top = {}
        self.top10 = {1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{}}

    def render(self, screen):
        ## top 10 general
        screen.blit(self.background, (0, SCREEN_HEIGHT * 0.6))
        for placement in self.top10:
            tmp_school = ""
            for school in self.top10[placement]["school"]:
                tmp_school += school + ", "
            score_tmp = self.font_score.render(str(self.top10[placement]["score"]) + ": " + str(tmp_school[:-2]), True, BLACK)
            placement_tmp = self.font_score.render(str(placement) + "." , True,BLACK)
            screen.blit(score_tmp, ((SCREEN_WIDTH * 0.5) - (score_tmp.get_rect().width / 2),
                                    SCREEN_HEIGHT * 0.65 + (placement - 1) * STAT_SIZE))
            screen.blit(placement_tmp, ((SCREEN_WIDTH * 0.1) - (placement_tmp.get_rect().width / 2),
                                    SCREEN_HEIGHT * 0.65  + (placement - 1) * STAT_SIZE))

        ## top ecole
        # nb_score = 0
        # for school in self.top:
        #     score_tmp = self.font_score.render(str(school) + ": " + str(self.top[school]), True, BLACK)
        #     if nb_score % 2 == 0:
        #         place = 0.25
        #     else:
        #         place = 0.75
        #     screen.blit(score_tmp, ((SCREEN_WIDTH * place) - (score_tmp.get_rect().width / 2), SCREEN_HEIGHT / 2 + 300 + (nb_score // 2) * STAT_SIZE))
        #     nb_score += 1


    def reset(self, score_board):
        ## top 10
        tmp_liste = []
        for school in score_board:
            tmp_liste.extend(score_board[school])

        tmp_liste = sorted(list(dict.fromkeys(tmp_liste)), reverse = True)
        tmp_liste = tmp_liste + [0]*(len(score_board) - len(tmp_liste))

        for placement in range(1,11):
            self.top10[placement] = {"score":tmp_liste[placement - 1], "school":[]}
            for school in score_board:
                if tmp_liste[placement - 1] in score_board[school]:
                    self.top10[placement]["school"].append(school)

        ## top ecole
        for school in score_board:
            if len(score_board[school]) > 0:
                self.top[school] = max(score_board[school])
            else:
                self.top[school] = 0

    def insert_element(self, liste):
        return liste