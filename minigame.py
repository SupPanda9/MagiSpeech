import pygame
from settings import *
from random import randint, choice
import sliding_puzzle
import millionaire

class MiniGame:
    """
    Controller class for managing and executing mini-games within
    the game environment.

    Parameters:
    - world: An instance of the World class representing the game
    world containing the mini-game.

    Attributes:
    - world: An instance of the World class representing the game.

    Methods:
        run(): Executes a randomly selected mini-game from a 
        predefined list and updates the game state based on the outcome.
    """
    def __init__(self, world):
        """
        Initialize the MiniGame instance.

        Parameters:
        - world (World): The World instance containing the mini-game.
        """
        self.world = world

    def run(self):
        """
        Run a randomly selected mini-game and add experience from
        it to the player.
        """
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