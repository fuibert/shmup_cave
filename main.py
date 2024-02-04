import game
from io_cave import *

while not game.exit_requested():
    if not verre():
        game.reset()
        game.running = False
    
    game.loop()

    if game.ended:
        reward(game.score)