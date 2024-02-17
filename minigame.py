import pygame
from settings import *
from random import randint, choice
import sliding_puzzle
import millionaire

class MiniGame:
    def __init__(self, world):
        # self.display_surface = pygame.display.get_surface()
        self.world = world

    def run(self):
        games = [sliding_puzzle.Game, millionaire.Game]
        selected_game = choice(games)
        
        game_instance = selected_game(self.world)
        game_instance.run()
        self.world.mini_game_active = False

        if self.world.solved_mini_game:
            if isinstance(game_instance, sliding_puzzle.Game):
                self.world.add_xp(minigame_stats["sliding_puzzle"])
            else:
                self.world.add_xp(self.world.game_correct_answers * minigame_stats["millionaire"])

        self.world.solved_mini_game = False
        self.world.game_correct_answers = 0