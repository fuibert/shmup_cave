import Game_class
from const import GAME_STATE
from io_cave import *

game = Game_class.Game()

while not game.exit_requested():
    if not verre():
        game.reset()
    
    game.loop()

    if game.state == GAME_STATE.ENDED:
        reward(game.score)
        game.reset()