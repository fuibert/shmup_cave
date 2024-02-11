import pygame.sprite
import json
import random
from const import *

class Bonus(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        with open("bonus_attributes.json", "r") as f:
            self.bonus = json.loads(f.read())
        self.reset()
    def reset(self):
        self.params = self.bonus[self.draw_bonus_key()]
        self.image_base = pygame.image.load("textures/bonus/" + self.params["sprite"])
        self.start_position = random.randrange(0, SCREEN_WIDTH)
        self.pos = pygame.math.Vector2(self.start_position, -10)
        self.speed = pygame.math.Vector2(0, self.params["speed"] * SCREEN_HEIGHT)
        self.image = pygame.transform.scale_by(self.image_base, 2)
        self.surf = pygame.Surface((self.params["size_x"] * 2, self.params["size_y"] * 2))
        self.rect = self.surf.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        self.healing = self.params["healing"]
        self.attack_speed_modifier = self.params["attack_speed_modifier"]
        self.plane_speed_modifier = self.params["plane_speed_modifier"]
        self.duration = self.params["duration"]
        return

    def move(self):
        self.pos = self.pos + self.speed / FPS
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self):
        self.move()

    def render(self, screen):
        screen.blit(self.get_current_image(), self.rect)

    def draw_bonus_key(self):
        bonus_weight = []
        bonus_name = []
        for curr_bonus_key, curr_bonus_value in self.bonus.items():
            bonus_weight.append(int(curr_bonus_value["weight"]))
            bonus_name.append(curr_bonus_key)
        return random.choices(bonus_name, weights=bonus_weight, k=1)[0]

    def get_current_image(self):
        return self.image