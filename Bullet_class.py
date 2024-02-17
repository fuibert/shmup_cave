import pygame
from Moving_elt_class import Moving_elt
from const import *

class Bullet(Moving_elt):
    def __init__(self, pos, direction, path, damage):
        self.damage = damage
        super().__init__(
            "bullets/" + path,
            0.03,
            pos,
            -direction,
            pygame.math.Vector2( 0, BULLET_SPEED * SCREEN_HEIGHT).rotate(direction)
        )

    def update(self):
        super().move()
        if self.is_out_of_bounds():
            self.kill()




