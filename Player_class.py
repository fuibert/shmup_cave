import pygame
from const import *
from Bullet_class import *
from Control_class import *
import Utils_class as utils


class Player(pygame.sprite.Sprite):
    def __init__(self, joystick):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/planes/" + PLAYER_IMAGE)
        self.image = pygame.transform.scale_by(self.image, 3)
        self.hitted_image = utils.make_hitted_image(self.image)
        self.hitted = 0
        self.surf = pygame.Surface((52 * 3, 52 * 3))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.hearth_image = pygame.image.load('textures/' + HEARTH_IMAGE)
        self.hearth_image = pygame.transform.scale_by(self.hearth_image, 0.1)
        self.health_rect = self.hearth_image.get_rect(center=(15, 15))

        self.school = "CAVE"

        self.max_length = 50

        self.control = Control(joystick)

    def move(self):
        if self.rect.left > 0 and self.control.left():
            self.rect.move_ip(-self.speed / FPS, 0)
        if self.rect.right < SCREEN_WIDTH and self.control.right():
            self.rect.move_ip(self.speed / FPS, 0)
        if self.rect.top > 0 and self.control.up():
            self.rect.move_ip(0, -self.speed / FPS)
        if self.rect.bottom < SCREEN_HEIGHT and self.control.down():
            self.rect.move_ip(0, self.speed / FPS)

    def render(self, screen):
        screen.blit(self.get_current_image(), self.rect)

    def update(self, bullets):
        if self.health <= 0:
            self.kill()
            return
        self.move()

        pressed_keys = pygame.key.get_pressed()

        if self.control.shoot():
            self.shoot(bullets)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > SHOOT_DELAY:
            self.lastShoot = now
            bullets.add(Bullet(self.rect.left + self.rect.width / 2, self.rect.top, 180, BULLET_PLAYER))

    def hit(self):
        self.health -= BULLET_ATTACK
        self.hitted = pygame.time.get_ticks()
        if self.health <= 0:
            self.reset()
            return False
        else:
            return True

    def get_current_image(self):
        now = pygame.time.get_ticks()
        if self.hitted != 0 and now - self.hitted < PLAYER_HITTED_DURATION:
            return self.hitted_image
        else:
            self.hitted = 0
            return self.image

    def render_health_bar(self, surface):
        surface.blit(self.hearth_image, self.hearth_image.get_rect())
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(46, 6, PLAYER_HEALTH + 58, 27), 2)
        bar_position = [50, 10, self.health + 50, 20]
        pygame.draw.rect(surface, GREEN, bar_position)

    def reset(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.health = PLAYER_HEALTH
