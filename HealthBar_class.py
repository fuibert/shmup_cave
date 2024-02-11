import pygame
from const import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width):
        self.image = pygame.image.load('textures/' + HEARTH_IMAGE)
        self.image = pygame.transform.scale_by(self.image, 0.1)
        self.rect = self.image.get_rect()
        self.width = width

        self.health = 1

    def update(self, health):
        self.health = health

    def render(self, screen, top, left):
        self.rect.top = top -10
        self.rect.right = left - 3
        screen.blit(self.image, self.rect)

        points=[
            (left - 2, top),
            (left + self.width + 2, top),
            (left + self.width + 2, top + 2 + 15 + 2),
            (left - 2, top + 2 + 15 +2)
            ]

        pygame.draw.lines(screen, BLACK, True, points)
        bar_position = [left, top + 2, self.width * self.health, 15]
        pygame.draw.rect(screen, GREEN, bar_position)
