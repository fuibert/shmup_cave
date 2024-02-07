import pygame
from const import *
from Background_class import *
from Player_class import *
from Enemy_class import *

class Game():
    def __init__(self):
        super().__init__() 
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.reset()

        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 30)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.waiting_verre = [self.font.render("Placer un verre", True, BLACK),
                              self.font.render("pour demarrer", True, BLACK)]

    def reset(self):
        self.running = False
        self.score = 0
        self.ended = False
        self.player = Player()
        self.background = Background()
        self.playerBullets = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def check_exit(self):
        if not pygame.get_init():
            return False
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            return True

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def display_waiting(self):
        self.screen.blit(self.waiting_verre[0], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 + 15))
        self.screen.blit(self.waiting_verre[1], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 - 15))

    def render(self):
        self.background.render(self.screen)
            
        if not self.running:
            self.player.render(self.screen)
            self.display_waiting()
            return

        for enemy in self.enemies:
            enemy.render(self.screen)

        for bullet in self.playerBullets:
            bullet.render(self.screen)

        for bullet in self.enemyBullets:
            bullet.render(self.screen)

        self.player.render(self.screen)
        return

    def exit_requested(self):
        return not pygame.get_init()

    def update(self):
        if not self.running:
            if pygame.key.get_pressed()[K_SPACE]:
                self.running = True

        self.background.animate(self.running)
        self.background.update()

        if self.ended:
            for enemy in self.enemies:
                enemy.kill()
            for bullet in self.enemyBullets:
                bullet.kill()
            for bullet in self.playerBullets:
                bullet.kill()
            return

        if self.running:
            for bullet in self.playerBullets:
                bullet.update()

            for bullet in self.enemyBullets:
                bullet.update()

            for enemy in self.enemies:
                enemy.update(self.enemyBullets)

            self.player.update(self.playerBullets)
            
            for hit in pygame.sprite.spritecollide(self.player, self.enemyBullets, False):
                self.ended = not self.player.hit()
                hit.kill()

            for enemy in self.enemies:
                for hit in pygame.sprite.spritecollide(enemy, self.playerBullets, False):
                    self.score += enemy.hit()
                    hit.kill()

            if(len(self.enemies) == 0):
                self.enemies.add(Enemy())

    def loop(self):
        if self.check_exit():
            return

        # fill the screen with a color to wipe away anything from last frame
        self.update()
        # RENDER YOUR GAME HERE
        self.render()

        # flip() the display to put your work on screen
        pygame.display.flip()
    
        self.clock.tick(FPS)  # limits FPS to 60
