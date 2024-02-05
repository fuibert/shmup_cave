import pygame
from pygame.locals import *
from const import *
from Bullet_class import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("textures/" + PLAYER_IMAGE)
        self.surf = pygame.Surface((52, 52))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.speed = 5 * 60
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip( -self.speed / FPS, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip( self.speed / FPS, 0)

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, bullets):
        self.move()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.lastShoot > SHOOT_DELAY: 
                self.lastShoot = now
                bullets.add(Bullet(self.rect.left + self.rect.width / 2, self.rect.top))


