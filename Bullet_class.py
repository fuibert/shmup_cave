import pygame
from const import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/bullet.png")
        self.surf = pygame.Surface((9, 5))
        self.rect = self.surf.get_rect()
        self.rect.update((X - 3, Y - 9), (9, 5))
        self.speed = ( 0, -10 * 60)

    def move(self):
        self.rect.move_ip(self.speed[0] / FPS, self.speed[1] / FPS)

    def render(self, screen):
         screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        if self.rect.bottom < 0:
            self.kill()




