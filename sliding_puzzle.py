import pygame
from random import choice, randint
import textwrap
from settings import *

TILE_SIZE = 200
TILE_NUM = 3
PUZZLE_SIZE = TILE_SIZE * TILE_NUM

class Game:
    """
    Initialize the game and manage the puzzle-solving process.

    Parameters:
    - world: The instance of the game world.

    Attributes:
    - screen: The Pygame surface for rendering.
    - clock: Pygame clock object for controlling the frame rate.
    - world: The instance of the game world.
    - font: The font used for rendering text.
    """
    def __init__(self, world):
        """
        Initialize the game with the given world instance.

        Parameters:
        - world: The instance of the game world.
        """
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.world = world
        self.font = pygame.font.SysFont(UI_FONT, 32)

    def create_tiles(self):
        """
        Create the tiles for the sliding puzzle by
        subsurfacing the whole image into parts.
        
        Attributes:
        - image: The image used for the puzzle.
        - reference_image: The scaled reference image.
        - tiles: List containing Tile instances.
        """
        self.image = pygame.image.load(f'assets/sliding_puzzle/{randint(0,7)}.jpg')
        self.image = pygame.transform.scale(self.image, (PUZZLE_SIZE, PUZZLE_SIZE))
        self.reference_image = self.image
        self.reference_image = pygame.transform.scale(self.reference_image, (PUZZLE_SIZE/2, PUZZLE_SIZE/2))
        self.tiles = []
        for i in range(TILE_NUM):
            for j in range(TILE_NUM):
                tile = self.image.subsurface(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                self.tiles.append(Tile(self, tile, i, j))

    def run(self):
        """
        Run the sliding puzzle game loop.

        Events:
        - Arrow keys: Move the tiles.
        - Space: Shuffle the puzzle.
        - Escape: End the game.
        """
        self.create_tiles()
        self.frame = Frame(self, self.tiles)
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.frame.draw(self.screen)
            self.screen.blit(self.reference_image, (10, (self.screen.get_height() - PUZZLE_SIZE) // 2))

            lines = textwrap.wrap(f'You can move the tiles with the arrows and forfeit the game with Escape.', 30)
            y_offset = 0
            for line in lines:
                text = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(text, (10, (self.screen.get_height() - PUZZLE_SIZE) // 2 + PUZZLE_SIZE // 2 + 10 + y_offset))
                y_offset += text.get_height()

            for event in pygame.event.get():
                self.frame.handle_event(event)
            pygame.display.flip()

    def end_game(self):
        """End the sliding puzzle game."""
        pygame.time.wait(800)
        self.running = False
        self.world.solved_mini_game = self.frame.solved


class Tile:
    """
    Represent a single tile in the sliding puzzle.

    Parameters:
    - game: The instance of the Game class.
    - image: The image associated with the tile.
    - row: The row index of the tile in the puzzle grid.
    - col: The column index of the tile in the puzzle grid.

    Attributes:
    - image: The image associated with the tile.
    - game: The instance of the Game class.
    - row: The row index of the tile in the puzzle grid.
    - col: The column index of the tile in the puzzle grid.
    - puzzle_x: The x-coordinate of the puzzle grid.
    - puzzle_y: The y-coordinate of the puzzle grid.
    - x: The current x-coordinate of the tile.
    - y: The current y-coordinate of the tile.
    - rect: The rectangular area occupied by the tile.
    """
    def __init__(self, game, image, row, col):
        """Initialize a tile for the sliding puzzle."""
        self.image = image
        self.game = game
        self.row = row
        self.col = col
        self.puzzle_x = (self.game.screen.get_width() - PUZZLE_SIZE) // 2
        self.puzzle_y = (self.game.screen.get_height() - PUZZLE_SIZE) // 2
        self.x = self.puzzle_x + col * TILE_SIZE
        self.y = self.puzzle_y + row * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        """Draw the tile on the screen."""
        screen.blit(self.image, (self.x, self.y))

    def move(self, direction):
        """
        Move the tile in a given direction.

        Parameters:
        - direction: The direction to move the tile ('up', 'down', 'left', 'right').
        """
        if direction == 'up':
            self.row -= 1
        elif direction == 'down':
            self.row += 1
        elif direction == 'left':
            self.col -= 1
        elif direction == 'right':
            self.col += 1
        self.x = self.puzzle_x + self.col * TILE_SIZE
        self.y = self.puzzle_y + self.row * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)


class Frame:
    """
    Represent the frame, containing the tiles in the sliding puzzle.

    Parameters:
    - game: The instance of the Game class.
    - tiles: A list of Tile objects representing the tiles in the puzzle.

    Attributes:
    - tiles: A list of Tile objects representing the tiles in the puzzle.
    - empty_row: The row index of the empty tile.
    - empty_col: The column index of the empty tile.
    - shuffling: A boolean indicating whether the puzzle is currently being shuffled.
    - moves: The number of moves made by the player.
    - solved: A boolean indicating whether the puzzle has been solved.
    - font: The font used for rendering text.
    """
    def __init__(self, game, tiles):
        """Initialize the frame(grid) for the sliding puzzle."""
        self.tiles = tiles
        self.empty_row = TILE_NUM - 1
        self.empty_col = TILE_NUM - 1
        self.shuffling = False
        self.moves = 0
        self.solved = False
        self.font = pygame.font.SysFont('Arial', 32)
        self.shuffle()
        self.game = game

    def draw(self, screen):
        """Draw the frame on the screen."""
        screen.fill((255, 255, 255))
        if self.solved:
            for tile in self.tiles:
                tile.draw(screen)
        else:
            for tile in self.tiles[:-1]:
                tile.draw(screen)
        self.draw_text(screen)

    def draw_text(self, screen):
        """
        Draw text information on the screen about the moves
        that he player used and whetther he successfully solved it.

        Parameters:
        - screen: The Pygame surface for rendering.
        """
        text = self.font.render(f'Moves: {self.moves}', True, (0, 0, 0))
        screen.blit(text, (10, 10))
        if self.solved:
            text = self.font.render('You solved the puzzle!', True, (0, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
            self.game.running = False

    def shuffle(self):
        """
        Shuffle the tiles in the puzzle.
        """
        directions = ['up', 'down', 'left', 'right']
        for i in range(100):
            direction = choice(directions)
            self.move_tile(direction, True)
        self.shuffling = False
        self.moves = 0
        self.solved = False

    def move_tile(self, direction, shuffle=False):
        """
        Move a tile in the specified direction.

        Parameters:
        - direction: The direction in which to move the tile.
        - shuffle: A boolean indicating whether the shuffle mode is enabled.
        """
        if direction == 'up' and self.empty_row < TILE_NUM - 1:
            row = self.empty_row + 1
            col = self.empty_col
        elif direction == 'down' and self.empty_row > 0:
            row = self.empty_row - 1
            col = self.empty_col
        elif direction == 'left' and self.empty_col < TILE_NUM - 1:
            row = self.empty_row
            col = self.empty_col + 1
        elif direction == 'right' and self.empty_col > 0:
            row = self.empty_row
            col = self.empty_col - 1
        else:
            return
        
        for tile in self.tiles:
                if tile.row == row and tile.col == col:
                    tile.move(direction)
                    self.empty_row = row
                    self.empty_col = col
                    if not shuffle:
                        self.moves += 1
                        self.check_solution()
                    break
        
    def check_solution(self):
        """
        Check if the puzzle has been solved.
        """
        for i, tile in enumerate(self.tiles):
            row = i // TILE_NUM
            col = i % TILE_NUM
            if tile.row != row or tile.col != col:
                return
        self.solved = True
        self.draw(self.game.screen)
        pygame.display.flip()
        self.game.end_game()

    def handle_event(self, event):
        """
        Handle user input events.

        Parameters:
        - event: The Pygame event object.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()
            elif event.key == pygame.K_UP:
                self.move_tile('up')
            elif event.key == pygame.K_DOWN:
                self.move_tile('down')
            elif event.key == pygame.K_LEFT:
                self.move_tile('left')
            elif event.key == pygame.K_RIGHT:
                self.move_tile('right')
            elif event.key == pygame.K_SPACE:
                self.shuffling = True
                self.shuffle()