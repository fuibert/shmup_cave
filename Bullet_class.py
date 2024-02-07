import pygame
from const import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, X, Y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/" + BULLET_IMAGE)
        self.surf = pygame.Surface((9, 5))
        self.rect = self.surf.get_rect()
        self.rect.update((X - 3, Y - 9), (9, 5))
        self.speed = pygame.math.Vector2( 0, BULLET_SPEED)
        self.speed.rotate_ip(direction)
        self.pos = pygame.math.Vector2(X - 3, Y - 9)

    def move(self):
        self.pos = self.pos + self.speed / FPS
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def render(self, screen):
         screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        if self.rect.bottom < 0:
            self.kill()




