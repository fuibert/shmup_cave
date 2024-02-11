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
        self.surf = pygame.Surface((52 * 3, 52 * 3))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        
        self.healthBar = HealthBar(self.rect.width)

        self.health_state = HEALTH_STATE.ALIVE
        self.animation = ANIMATION_STATE.IDLE

        self.school = "CAVE"

        self.max_length = 50

        self.control = Control(joystick)

    def move(self):
        if self.animation == ANIMATION_STATE.IDLE:
            return

        if self.animation == ANIMATION_STATE.ANIMATED:
            self.rect.move_ip(0, -self.speed * 1.5 / FPS)
            if (self.rect.center[1] <= SCREEN_HEIGHT * 0.8):
                self.animation = ANIMATION_STATE.PLAYABLE
            return



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
        if self.animation == ANIMATION_STATE.PLAYABLE:
            self.healthBar.render(screen, self.rect.bottom, self.rect.left)

    def update(self, bullets):
        self.move()

        if self.animation != ANIMATION_STATE.PLAYABLE:
            return

        if self.health <= 0:
            self.kill()
            return

        if self.control.shoot():
            self.shoot(bullets)

        self.healthBar.update(self.health / PLAYER_HEALTH)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > SHOOT_DELAY:
            self.lastShoot = now
            bullets.add(Bullet(self.rect.left + self.rect.width / 2, self.rect.top, 180, BULLET_PLAYER, BULLET_ATTACK))

    def hit(self, dammage):
        self.health -= dammage
        self.hitted = pygame.time.get_ticks()
        if self.health <= 0:
            self.explode()

    def die(self):
        self.health_state = HEALTH_STATE.DEAD
        # self.reset()

    def explode(self):
        if self.explode_time == 0:
            self.explode_time = pygame.time.get_ticks()

    def is_alive(self):
        return self.health_state == HEALTH_STATE.ALIVE

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
        else:
            self.hitted = 0
            return self.image

    def reset(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))
        self.lastShoot = 0
        self.hitted = 0
        self.explode_time = 0
        self.health = PLAYER_HEALTH
        self.animation = ANIMATION_STATE.IDLE


    def animate(self):
        self.animation = ANIMATION_STATE.ANIMATED
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1.1))
