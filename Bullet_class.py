import pygame
from const import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, X, Y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/" + BULLET_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.update(
            (X - self.rect.width / 2, Y - self.rect.height / 2), 
            (self.rect.width, self.rect.height)
        )
        self.speed = pygame.math.Vector2( 0, BULLET_SPEED)
        self.speed.rotate_ip(direction)
        self.pos = pygame.math.Vector2(X - self.rect.width / 2, Y - self.rect.height / 2)

    def move(self):
        self.pos = self.pos + self.speed / FPS
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def render(self, screen):
         screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        if self.rect.bottom < 0:
            self.kill()




