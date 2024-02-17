import pygame
from Control_class import Control
from HealthBar_class import HealthBar
from Plane_class import Plane
from const import *

class Player(Plane):
    def __init__(self, attributes, joystick):               
        self.animation = ANIMATION_STATE.IDLE

        self.school = "CAVE"

        #self.max_length = 50
        self.lin_speed = attributes["speed"]        

        self.control = Control(joystick)
        self.bonus_time =0
        self.bonus_image = utils.make_bonus_image(self.image)
        self.shoot_delay = SHOOT_DELAY

        self.arrows = []
        arrow = pygame.transform.scale_by(pygame.image.load("textures/arrow.png"), 1)

        self.tuto_time = 0

        for i in range(4):
            self.arrows.append(pygame.transform.rotate(arrow, i * 90))

        super().__init__(attributes, pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8), 0, 0) 
        self.max_health = attributes["health"]        
        self.healthBar = HealthBar(self.rect.width)           

    def move(self):
        if self.animation == ANIMATION_STATE.IDLE:
            self.speed = pygame.math.Vector2(0, 0)

        elif self.animation == ANIMATION_STATE.ANIMATED:
            self.speed = pygame.math.Vector2(0, -self.lin_speed * 1.5 * SCREEN_HEIGHT)
          
        else:
            self.speed = pygame.math.Vector2(self.control.direction()) * self.lin_speed * SCREEN_HEIGHT
            
        super().move()        

    def blit(self, screen):
        super().blit(screen)
        if self.animation == ANIMATION_STATE.PLAYABLE:
            self.healthBar.render(screen, self.rect.bottom, self.rect.left)

        if self.animation == ANIMATION_STATE.TUTO:
            if pygame.time.get_ticks() % 500 < 250:
                offset = pygame.math.Vector2(self.rect.width * 0.8, 0)
                for i in range(4):
                    arrow = self.arrows[i].get_rect(center = (self.rect.center + offset))
                    screen.blit(self.arrows[i], arrow)
                    offset.rotate_ip( -90)


    def update(self, bullets):
        if self.animation == ANIMATION_STATE.ANIMATED and self.rect.center[1] <= SCREEN_HEIGHT * 0.8:
            self.animation = ANIMATION_STATE.TUTO
            self.tuto_time = pygame.time.get_ticks()
            return

        if self.animation == ANIMATION_STATE.TUTO:
            if pygame.time.get_ticks() - self.tuto_time > TUTO_DURATION:
                self.animation = ANIMATION_STATE.PLAYABLE

        if self.control.shoot():
            super().shoot(bullets)

        super().update()
        self.limit_to_bounds()   

        self.healthBar.update(self.health / self.max_health)

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

    def animate(self):
        self.animation = ANIMATION_STATE.ANIMATED
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1.1))

    def limit_to_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def kill(self):
        self.health_state = HEALTH_STATE.DEAD
        super().kill()        