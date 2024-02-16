import pygame, sys
from settings import *
from level import World, Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("MagiSpeech")
        self.clock = pygame.time.Clock()

        self.world = World()

    def run(self):
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