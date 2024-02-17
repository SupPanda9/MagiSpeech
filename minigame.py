import pygame
from settings import *
from random import randint
import sliding_puzzle
import millionaire

class MiniGame:
    def __init__(self, world):
        
        # ((2 * WIDTH / 3, 2 * HEIGHT / 3))
        self.display_surface = pygame.display.get_surface()

        # self.x = (WIDTH - 2 * WIDTH / 3) / 2
        # self.y = (HEIGHT - 2 * HEIGHT / 3) / 2

        self.world = world

    def run(self):
        """self.world.solved_mini_game = False
        sliding_game = sliding_puzzle.Game(self.world)
        sliding_game.run()
        if self.world.solved_mini_game:
            print("yes, solved it")
            """
        millionaire_game = millionaire.Game(self.world)
        millionaire_game.run()
        self.world.mini_game_active = False