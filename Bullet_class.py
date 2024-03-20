import pygame
from Moving_elt_class import MovingElement
from const import BULLET_SIZE_RATIO,BULLET_SPEED,SCREEN_HEIGHT

class Bullet(MovingElement):
    def __init__(self, pos, direction, path, damage, size=0.03):
        self.damage = damage
        super().__init__(
            "bullets/" + path,
            size * BULLET_SIZE_RATIO,
            pos,
            -direction,
            pygame.math.Vector2( 0, BULLET_SPEED * SCREEN_HEIGHT).rotate(direction)
        )

    def update(self):
        super().move()
        if self.is_out_of_bounds():
            self.kill()




