import pygame
from const import *
from Bullet_class import *
from Control_class import *
from HealthBar_class import *
import Utils_class as utils


class Player(pygame.sprite.Sprite):
    def __init__(self, joystick):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/planes/" + PLAYER_IMAGE)
        self.image = pygame.transform.scale_by(self.image, 3)
        self.hitted_image = utils.make_hitted_image(self.image)
        self.hitted = 0
        self.explosion_images = utils.load_explosions_sprites()
        self.explode_time = 0
        self.alive = True
        self.surf = pygame.Surface((52 * 3, 52 * 3))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH

        self.healthBar = HealthBar(self.rect.width)

        self.school = "CAVE"

        self.max_length = 50

        self.control = Control(joystick)
        self.bonus_time =0
        self.bonus_image = utils.make_bonus_image(self.image)
        self.shoot_delay = SHOOT_DELAY

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
        self.healthBar.render(screen, self.rect.bottom, self.rect.left)

    def update(self, bullets):
        if self.health <= 0:
            self.kill()
            return
        self.move()
        self.update_bonus()

        pressed_keys = pygame.key.get_pressed()

        if self.control.shoot():
            self.shoot(bullets)

        self.healthBar.update(self.health / PLAYER_HEALTH)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > self.shoot_delay:
            self.lastShoot = now
            bullets.add(Bullet(self.rect.left + self.rect.width / 2, self.rect.top, 180, BULLET_PLAYER, BULLET_ATTACK))

    def hit(self, dammage):
        self.health -= dammage
        self.hitted = pygame.time.get_ticks()
        if self.health <= 0:
            self.explode()

    def die(self):
        self.alive = False
        # self.reset()

    def explode(self):
        if self.explode_time == 0:
            self.explode_time = pygame.time.get_ticks()

    def is_alive(self):
        return self.alive

    def get_current_image(self):
        now = pygame.time.get_ticks()
        if self.hitted != 0 and now - self.hitted < PLAYER_HITTED_DURATION:
            return self.hitted_image
        elif self.explode_time !=0 :
            explosion_step = round((now - self.explode_time) // 100)
            if explosion_step >= (len(self.explosion_images) - 1) % PLAYER_EXPLODE_STEPS:
                explosion_step = len(self.explosion_images) - 1
                self.die()
            return self.explosion_images[explosion_step]
        elif self.bonus_time != 0:
            return self.bonus_images
        else:
            self.hitted = 0
            return self.image

    def reset(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.hitted = 0
        self.explode_time = 0
        self.health = PLAYER_HEALTH

    def add_bonus(self, bonus):
        if self.bonus_time == 0:
            self.bonus_time = pygame.time.get_ticks()
            self.shoot_delay = self.shoot_delay / bonus.attack_speed_modifier
            self.speed = self.shoot_delay / bonus.plane_speed_modifier
            self.health = self.health + bonus.healing
            self.bonus_duration = bonus.duration

    def update_bonus(self):
        if self.bonus_time != 0 and pygame.time.get_ticks() - self.bonus_time < self.bonus_duration:
            self.bonus_time = 0
            self.shoot_delay = SHOOT_DELAY
            self.speed = PLAYER_SPEED
