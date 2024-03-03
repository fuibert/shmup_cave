import pygame
from const import *

class HealthBar(pygame.sprite.WeakSprite):
    def __init__(self, width):
        self.image = pygame.image.load('textures/' + HEARTH_IMAGE)
        self.image = pygame.transform.scale_by(self.image, 0.1)
        self.rect = self.image.get_rect()
        self.width = width

        self.health = 1

    def update(self, health):
        self.health = health

    def render(self, screen, top, left):
        THICKNESS = 3
        self.rect.top = top -10
        self.rect.right = left - 3
        screen.blit(self.image, self.rect)

        bar_position = [left, top, self.width * self.health, 15]
        pygame.draw.rect(screen, GREEN, bar_position)

        points=[
            (left, top),
            (left + self.width, top),
            (left + self.width, top + 15),
            (left, top + 15)
            ]

        pygame.draw.lines(screen, BLACK, True, points, width = THICKNESS)
