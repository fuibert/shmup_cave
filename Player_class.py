from numpy import minimum
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
        self.lin_speed_def = attributes["speed"] 
        self.lin_speed = self.lin_speed_def       

        self.control = Control(joystick)
        self.bonus_time =0
        #self.bonus_image = utils.make_bonus_image(self.image)
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
        if self.health_state == HEALTH_STATE.DEAD:
            return                    
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

        self.update_bonus()

        if self.control.shoot():
            super().shoot(bullets)

        super().update()
        self.limit_to_bounds()   

        self.healthBar.update(self.health / self.max_health)

    def add_bonus(self, bonus):
        if self.bonus_time == 0:
            self.bonus_time = pygame.time.get_ticks()
            self.cadence = self.cadence / bonus.effect["attack_speed_modifier"]
            self.lin_speed = self.lin_speed * bonus.effect["plane_speed_modifier"]
            self.health = minimum(self.health + bonus.effect["healing"], self.max_health)
            self.bonus_duration = bonus.effect["duration"]
            self.show_bonus_mask = True

    def update_bonus(self):
        if self.bonus_time != 0 and pygame.time.get_ticks() - self.bonus_time > self.bonus_duration:
            self.bonus_time = 0
            self.cadence = self.CADENCE
            self.lin_speed = self.lin_speed_def
            self.show_bonus_mask = False

    def animate(self):
        self.animation = ANIMATION_STATE.ANIMATED
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1.1))

    def limit_to_bounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT

    def kill(self):
        self.health_state = HEALTH_STATE.DEAD
        self.health = 0        
        super().kill()

    def set_player_school(self, school):
        self.school = school