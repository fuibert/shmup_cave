import math
from random import randint, randrange
import pygame
from const import *
from Bullet_class import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.reset()

    def reset(self):
        self.type = randint( 0, len(ENEMY_IMAGES) - 1)
        self.image_base = pygame.transform.rotate(
            pygame.image.load("textures/" + ENEMY_IMAGES[self.type]), 180.0)
        
        self.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, 25)
        self.speed = pygame.math.Vector2( 0, 200)
        self.direction = randrange( -25000, 25000) / 1000
        self.speed.rotate_ip( -self.direction)
        self.image = pygame.transform.rotate(self.image_base, self.direction)

        self.surf = pygame.Surface((52, 52))
        self.rect = self.surf.get_rect(center = (round(self.pos.x), round(self.pos.y)))

        self.lastShoot = 0

        self.health = ENEMY_HEALTH * (self.type / 10)
        self.points = self.health

    def move(self):
        self.pos = self.pos + self.speed / FPS
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()
        if self.rect.right < 0:
            self.reset()
        if self.rect.left > SCREEN_WIDTH:
            self.reset()


    def update(self, bullets):
        if self.health <= 0:
            self.kill()
            return
        self.move()
        self.shoot(bullets)
        
    def render(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > SHOOT_DELAY: 
            self.lastShoot = now
            direct = pygame.math.Vector2(self.speed.normalize()) * self.rect.width / 2
            pos = pygame.math.Vector2(self.pos) + direct
            bullets.add(Bullet(pos.x, pos.y, -self.direction))

    def hit(self):
        self.health -= BULLET_ATTACK
        if self.health <= 0:
            return self.points
        else:
            return 0