import random
import pygame
from Moving_elt_class import MovingElement
from const import SCREEN_HEIGHT, SCREEN_WIDTH

class Bonus(MovingElement):

    def __init__(self, attributes):
        super().__init__("bonus/" + attributes["sprite"],
                         attributes["size"],
                          pygame.math.Vector2(random.randrange(0, SCREEN_WIDTH), -10),
                          0,
                          pygame.math.Vector2(0, attributes["speed"] * SCREEN_HEIGHT))
        
        self.effect = attributes["effect"]

    def update(self):
        super().move()
        if self.is_out_of_bounds():
            self.kill()