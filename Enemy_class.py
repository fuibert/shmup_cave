import math
from random import randint, randrange
import pygame
from Plane_class import Plane
from const import SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(Plane):
    def __init__(self, attributes):
        pos = pygame.math.Vector2(randrange(0, SCREEN_WIDTH), -10)
        angle = self.start_angle(pos)
        
        self.points = attributes["score"]
        
        super().__init__(attributes,
                         pos,
                         180 + angle,
                         pygame.math.Vector2( 0, attributes["speed"] * SCREEN_HEIGHT).rotate( -  angle)
        )

    def start_angle(self, pos):
        # calcul de l'angle à gauche de l'avion
        left_AC = pos.x
        left_AB = SCREEN_HEIGHT
        left_degree = -round(int(math.degrees(math.atan(left_AC / left_AB))), 2)

        # calcul de l'angle à droite de l'avion
        rigth_AC = SCREEN_WIDTH - pos.x
        rigth_AB = SCREEN_HEIGHT
        rigth_degree = round(int(math.degrees(math.atan(rigth_AC/ rigth_AB))), 2)

        return randrange(left_degree,rigth_degree)

    def passed(self):
        return self.rect.top > SCREEN_HEIGHT

    def update(self, bullets):
        super().shoot(bullets)        
        super().update()