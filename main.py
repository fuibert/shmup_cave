import Game_class
from const import GAME_STATE, SKIP_IO
from io_cave import *
from fake_io_cave import *

if SKIP_IO:
    IO_Controller = Fake_IO_Controller()
else :
    IO_Controller = IO_Controller()

game = Game_class.Game()

while not game.exit_requested():
    if not IO_Controller.verre():
        game.idleMode()
        print("en attente d'un verre")
        time.sleep(0.1)
    if IO_Controller.verre() and game.isIdle():
        game.menuMode()

    game.loop()

    if game.state == GAME_STATE.ENDED:
        game.rewardMode()
        game.loop()
        IO_Controller.reward(game.score)
        game.reset()