import pygame
from random import choice

TILE_SIZE = 200
TILE_NUM = 3
PUZZLE_SIZE = TILE_SIZE * TILE_NUM

class Game:
    def __init__(self, world):
        self.screen = pygame.display.get_surface()
        # pygame.display.set_caption('Sliding Puzzle')
        self.clock = pygame.time.Clock()
        self.world = world

    def create_tiles(self):
        image = pygame.image.load('assets/map/level_0.png')
        image = pygame.transform.scale(image, (PUZZLE_SIZE, PUZZLE_SIZE))
        self.tiles = []
        for i in range(TILE_NUM):
            for j in range(TILE_NUM):
                tile = image.subsurface(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                self.tiles.append(Tile(self, tile, i, j))
        self.tiles.pop()

    def run(self):
        self.create_tiles()
        self.frame = Frame(self, self.tiles)
        self.running = True
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                self.frame.handle_event(event)
            self.frame.draw(self.screen)
            pygame.display.flip()

    def end_game(self):
        pygame.time.wait(400)
        self.running = False
        self.world.solved_mini_game = self.frame.solved


class Tile:
    def __init__(self, game, image, row, col):
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
        screen.blit(self.image, (self.x, self.y))

    def move(self, direction):
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
    def __init__(self, game, tiles):
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
        screen.fill((255, 255, 255))
        for tile in self.tiles:
            tile.draw(screen)
        self.draw_text(screen)

    def draw_text(self, screen):
        text = self.font.render(f'Moves: {self.moves}', True, (0, 0, 0))
        screen.blit(text, (10, 10))
        if self.solved:
            text = self.font.render('You solved the puzzle!', True, (0, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

    def shuffle(self):
        directions = ['up', 'down', 'left', 'right']
        for i in range(100):
            direction = choice(directions)
            self.move_tile(direction, True)
        self.shuffling = False
        self.moves = 0
        self.solved = False

    def move_tile(self, direction, shuffle=False):
        if not self.shuffling and self.solved:
            return
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
        for i, tile in enumerate(self.tiles):
            row = i // TILE_NUM
            col = i % TILE_NUM
            if tile.row != row or tile.col != col:
                return
        self.solved = True

    def handle_event(self, event):
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
        if self.solved:
            self.game.end_game()
