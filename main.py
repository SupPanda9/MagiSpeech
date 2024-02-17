import pygame, sys
from settings import *
from level import World, Level


class Game:
    """
    The main game class, responsible for initializing Pygame, managing the game loop,
    handling user input, and updating the game world.

    Attributes:
    - screen: Pygame window surface.
    - clock: Pygame clock object for controlling frame rate.
    - world: Instance of the game world containing levels, player, and other game state related data.
    """
    def __init__(self):
        """
        Initialize the Game object by setting up Pygame window, caption, and clock,
        and creating the game world.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("MagiSpeech")
        self.clock = pygame.time.Clock()

        self.world = World()

    def run(self):
        """
        Handle events, update the game world, and render the game.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.world.start_mini_game()
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.world.mini_game_active = False

            self.screen.fill("black")
            self.world.level.run() 

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()