import pygame
from pygame.locals import *
from const import *
from Bullet_class import *

class Player(pygame.sprite.Sprite):
    def __init__(self, joystick):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("textures/" + PLAYER_IMAGE)
        self.image = pygame.transform.scale_by(self.image, 3)
        self.surf = pygame.Surface((52 * 3, 52 * 3))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.hearth_image = pygame.image.load('textures/' + HEARTH_IMAGE)
        self.hearth_image = pygame.transform.scale_by(self.hearth_image, 0.1)
        self.health_rect = self.hearth_image.get_rect(center=(15,15))

        self.school = "CAVE"

        self.max_length = 50

        self.joystick = joystick

    def move(self):
        pressed_keys = pygame.key.get_pressed()         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT] or self.joystick != None and self.joystick.get_axis(0) < -0.5:
                  self.rect.move_ip( -self.speed / FPS, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT] or self.joystick != None and self.joystick.get_axis(0) > 0.5:
                  self.rect.move_ip( self.speed / FPS, 0)
        if self.rect.bottom > 0:
            if pressed_keys[K_UP] or self.joystick != None and self.joystick.get_axis(1) < -0.5:
                self.rect.move_ip(0, -self.speed / FPS)
        if self.rect.top < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN] or self.joystick != None and self.joystick.get_axis(1) > 0.5:
                self.rect.move_ip(0, self.speed / FPS)

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, bullets):
        if self.health <= 0:
            self.kill()
            return
        self.move()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_SPACE]:
            self.shoot(bullets)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > SHOOT_DELAY: 
            self.lastShoot = now
            bullets.add(Bullet(self.rect.left + self.rect.width / 2, self.rect.top, 180))

    def hit(self):
        self.health -= BULLET_ATTACK
        if self.health <= 0:
            self.reset()
            return False
        else:
            return True

    def render_health_bar(self, surface):
        surface.blit(self.hearth_image, self.hearth_image.get_rect())
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(46, 6, PLAYER_HEALTH+58, 27), 2)
        bar_position = [50, 10, self.health+50 , 20]
        pygame.draw.rect(surface, GREEN, bar_position)


    def reset(self):
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.health = PLAYER_HEALTH


