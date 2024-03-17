import Game_class
from const import GAME_STATE
from io_cave import *

IO_Controller = IO_Controller()
game = Game_class.Game()

while not game.exit_requested():
    if not IO_Controller.verre():
        print("en attente d'un verre")
        time.sleep(0.1)
        game.reset()
    
    game.loop()

    if game.state == GAME_STATE.ENDED:
        IO_Controller.reward(game.score)
        game.reset()