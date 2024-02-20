import pygame
from const import SCREEN_WIDTH

class DrawableElement(pygame.sprite.Sprite):
    def __init__(self, image_path, width, angle, pos):
        self.set_image("textures/" + image_path, angle, width)
        self.pos = pos
        self.angle = angle        
        self.rect = self.image.get_rect(center=self.pos) 
        self.base_image = self.image 
        super().__init__()                 

    def set_image(self, path, angle, width):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = pygame.transform.scale(self.image, 
                            (width * SCREEN_WIDTH, self.image.get_height()  * SCREEN_WIDTH / self.image.get_width() * width))
        self.mask = pygame.mask.from_surface(self.image)
        self.show_mask = False
        
    def update(self):
        pass

    def blit(self, screen):
        screen.blit(self.image, self.rect)
        if self.show_mask:
            screen.blit(
                self.mask.to_surface(setcolor=pygame.Color(255,0,0,127),unsetcolor=pygame.Color(0,0,0,0)),
                self.rect)