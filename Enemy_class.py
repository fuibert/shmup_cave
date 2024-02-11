import math
from random import randint, randrange
import pygame
from const import *
from Bullet_class import *
import json
import Utils_class as utils

class Enemy(pygame.sprite.Sprite):

    with open("plane_attributes.json", "r") as f:
        planes = json.loads(f.read())

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.reset()

    def reset(self):
        self.type = randint( 1, len(Enemy.planes) - 1)
        self.plane = Enemy.planes['avion'+str(self.type)]
        self.image_base = pygame.transform.rotate(
            pygame.image.load("textures/planes/" + self.plane["sprite"]), 180.0)
        self.start_position = randrange(0, SCREEN_WIDTH)
        self.pos = pygame.math.Vector2(self.start_position, -10)
        self.speed = pygame.math.Vector2( 0, self.plane["speed"] * SCREEN_HEIGHT)
        self.direction = self.start_angle()
        self.speed.rotate_ip( -self.direction)
        self.image = pygame.transform.rotate(self.image_base, self.direction)
        self.image = pygame.transform.scale_by(self.image, 3)
        self.hitted_image = utils.make_hitted_image(self.image)
        self.hitted =0

        self.surf = pygame.Surface((52 * 3, 52 * 3))
        self.rect = self.surf.get_rect(center = (round(self.pos.x), round(self.pos.y)))

        self.lastShoot = 0

        self.health = self.plane["health"] * (self.type / 10)
        self.points = self.plane["score"]

    def start_angle(self):
        # calcul de l'angle à gauche de l'avion
        left_AC = self.start_position
        left_AB = SCREEN_HEIGHT
        left_degree = -round(int(math.degrees(math.atan(left_AC / left_AB))), 2)

        # calcul de l'angle à droite de l'avion
        rigth_AC = SCREEN_WIDTH - self.start_position
        rigth_AB = SCREEN_HEIGHT
        rigth_degree = round(int(math.degrees(math.atan(rigth_AC/ rigth_AB))), 2)

        return randrange(left_degree,rigth_degree)

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
        screen.blit(self.get_current_image(), self.rect)

    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > self.plane["cadence"]:
            self.lastShoot = now
            direct = pygame.math.Vector2(self.speed.normalize()) * self.rect.width / 2
            pos = pygame.math.Vector2(self.pos) + direct
            bullets.add(Bullet(pos.x, pos.y, -self.direction, self.plane["bullet"]))

    def hit(self):
        self.health -= self.plane["dammage"]
        self.hitted = pygame.time.get_ticks()
        if self.health <= 0:
            return self.points
        else:
            return 0

    def get_current_image(self):
        now = pygame.time.get_ticks()
        if self.hitted != 0 and now - self.hitted < ENEMY_HITTED_DURATION:
            return self.hitted_image
        else:
            self.hitted = 0
            return self.image