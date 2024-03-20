import pygame
import os
import json
from const import *

class Statistics(pygame.sprite.Sprite):
    def __init__(self):
        self.background = pygame.image.load('textures/background/bg_stat.png')
        self.background = pygame.transform.scale(self.background, 
                                                 (SCREEN_WIDTH, SCREEN_WIDTH * self.background.get_height() /self.background.get_width()))

        self.font_score = pygame.font.Font("src/fonts/" + STAT_FONT, STAT_SIZE)
        self.loadFile()

    def loadFile(self):
        with open("score_board.json", "r") as f:
            self.data = json.loads(f.read())
            self.score_board = self.data["all_scores"]
            self.top_scores = self.data["top_scores"]
    def render(self, screen):
        screen.blit(self.background, (0, SCREEN_HEIGHT * 0.6))
        tmp_list = {k: v for k, v in sorted(self.top_scores.items(), key=lambda item: item[1], reverse=True)}
        keys = list(tmp_list)
        for i in range(0, 10):
            placement = i+1
            score_tmp = self.font_score.render(str(keys[i]) + ": " + str(tmp_list[keys[i]]), True,
                                               BLACK)
            placement_tmp = self.font_score.render(str(placement) + "." , True,BLACK)
            screen.blit(score_tmp, ((SCREEN_WIDTH * 0.5) - (score_tmp.get_rect().width / 2),
                                    SCREEN_HEIGHT * 0.65 + (placement - 1) * STAT_SIZE))
            screen.blit(placement_tmp, ((SCREEN_WIDTH * 0.1) - (placement_tmp.get_rect().width / 2),
                                    SCREEN_HEIGHT * 0.65  + (placement - 1) * STAT_SIZE))

    def add_score(self, score, ecole):
        self.score_board[ecole].append(score)
        if self.top_scores[ecole] < score:
            self.top_scores[ecole] = score
        with open("score_board.json", "w") as f:
            f.write(json.dumps(self.data))

    def insert_element(self, liste):
        return liste