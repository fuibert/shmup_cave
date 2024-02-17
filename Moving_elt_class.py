from Drawable_elt_class import Drawable_elt
from const import *

class Moving_elt(Drawable_elt):
    def __init__(self, image_path, size, pos, angle, speed):
        self.speed = speed
        super().__init__(image_path, size, angle, pos)  

    def move(self):
        self.pos = self.pos + self.speed / FPS
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def is_out_of_bounds(self):       
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            return True   
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            return True 
        return False
                                                   
                     




