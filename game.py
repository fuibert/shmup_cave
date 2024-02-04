import pygame
from const import *
from Background_class import *
from Player_class import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
clock = pygame.time.Clock()
background = Background()
player = Player()

score = 0
running = False
ended = False

size = pygame.display.get_window_size()
print(size)

def reset():
    running = False
    score = 0
    ended = False

def check_exit():
    if not pygame.get_init():
        return False
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    return False

def display_waiting():
    return
    #screen.fill("green")

def render():
    background.render(screen)
    player.render(screen)
    if not running:
         display_waiting()
         return
    return

def exit_requested():
    return not pygame.get_init()

def update():
    if running:
        background.update()
    else:
        background.update()
        player.update()

def loop():
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    if check_exit():
        return
    # fill the screen with a color to wipe away anything from last frame
    update()
    # RENDER YOUR GAME HERE
    render()

    # flip() the display to put your work on screen
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60
