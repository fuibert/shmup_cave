import pygame
from const import *
from Background_class import *
from Player_class import *

class Game():
    def __init__(self):
        super().__init__() 
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.reset()

        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 40)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.waiting_verre = self.font.render("Placer un verre\npour demarrer", True, BLACK)

    def reset(self):
        self.running = False
        self.score = 0
        self.ended = False
        self.player = Player()
        self.background = Background()

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
        self.screen.blit(self.waiting_verre, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def render(self):
        self.background.render(self.screen)
        self.player.render(self.screen)
        if not self.running:
             self.display_waiting()
             return
        return

    def exit_requested(self):
        return not pygame.get_init()

    def update(self):
        if not self.running:
            if pygame.key.get_pressed()[K_SPACE]:
                self.running = True
        self.background.animate(self.running)
        self.background.update()
        if self.running:
            self.player.update()

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
