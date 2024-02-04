import Game_class
from io_cave import *

game = Game_class.Game()

while not game.exit_requested():
    if not verre():
        game.reset()
        running = False
    
    game.loop()

    if game.ended:
        reward(game.score)