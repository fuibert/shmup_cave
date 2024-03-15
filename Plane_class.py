import pygame
from Moving_elt_class import MovingElement
from const import *
from Bullet_class import Bullet

class Plane(MovingElement):
    def __init__(self, attributes, pos, angle, speed):
        self.lastShoot = 0
        self.cadence = attributes["cadence"]
        self.CADENCE = attributes["cadence"]
        self.bullet = attributes["bullet"]
        self.damage = attributes["damage"]        
        
        self.health = attributes["health"]
        
        self.hitted = 0

        self.health_state = HEALTH_STATE.ALIVE
        
        super().__init__("planes/" + attributes["sprite"],
                         attributes["size"],
                         pos,
                         angle,
                         speed
        )

    def update(self):
        self.move()
        self.show_mask = (self.health_state == HEALTH_STATE.HITTED)
        if pygame.time.get_ticks() - self.hitted > HITTED_DURATION:
            self.health_state = HEALTH_STATE.ALIVE
    
    def shoot(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > self.cadence:
            self.lastShoot = now
            direct = pygame.math.Vector2(0, self.rect.width / 2).rotate(180 - self.angle)
            pos = pygame.math.Vector2(self.pos) + direct
            bullets.add(Bullet(pos, 180 - self.angle, self.bullet, self.damage,self.size))

    def hit(self, bullet):
        self.receive_damage(bullet.damage)
        bullet.kill()

    def receive_damage(self, damage) :
        self.health -= damage                   
        self.hitted = pygame.time.get_ticks()
        if self.health <= 0:
            self.health_state = HEALTH_STATE.DEAD
        else:
            self.health_state = HEALTH_STATE.HITTED

    def is_alive(self):
        return self.health_state == HEALTH_STATE.ALIVE

    def is_hitted(self):
        return self.health_state == HEALTH_STATE.HITTED

    def is_dead(self):
        return self.health_state == HEALTH_STATE.DEAD    
