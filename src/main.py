### MODULE IMPORTS ###

import pygame
from game import Game
from helpers import install_missing_modules

### MAIN ###

required_modules = ["pygame-ce", "pytmx"]
install_missing_modules(required_modules)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

### END ###
