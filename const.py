from enum import Enum

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 120

SHOOT_DELAY = 400
BULLET_SPEED = 3

HITTED_DURATION = 150

#MAX = number of explosion sprite steps
ENEMY_EXPLODE_STEPS = 3
PLAYER_EXPLODE_STEPS = 7

BACKGROUND_IMAGE = 'background_1.png' #'bg_1440x960.png'
# BACKGROUND_IMAGE = 'bg_284x868.png'
PLAYER_IMAGE = 'plane5.png'
BULLET_PLAYER = 'bullet_4.png'
BULLET_IMAGE = 'bullet_1.png'
HEARTH_IMAGE = 'coeur.png'

SCORE_FONT = "Top_Secret_Stamp.ttf"
SCORE_SIZE = 100

STAT_FONT = "Top_Secret_Stamp.ttf"
STAT_SIZE = 55

HEALTH_STATE = Enum('health', [ 'ALIVE', 'HITTED', 'DEAD'])
ANIMATION_STATE = Enum('status', ['IDLE', 'ANIMATED', 'TUTO', 'PLAYABLE'])
GAME_STATE = Enum('state', ['MENU','IDLE', 'TUTO', 'RUNNING', 'ENDING', 'ENDED'])

TUTO_DURATION = 3000