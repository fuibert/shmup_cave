import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.images = []
        for i in range(1, 7 + 1) :
            self.images.append(pygame.image.load("textures/explosions/Explosion_" + str(i) + '.png'))
        self.pos = pos
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=self.pos)
        super().__init__()        

    def update(self):
        if self.index >= len(self.images):
            self.kill()
            return
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.pos)
        self.index += 1