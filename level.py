import pygame
from settings import *
from tile import Tile
from player import Player
from helpers import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        # groups of sprites with different behavior
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("assets/map/level_0_FloorBlocks.csv"),
        }

        for style, layout in layouts.items():       
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if style == "boundary":
                            Tile((x,y), [self.obstacle_sprites], "black")
                        

        self.player = Player((1200,2400), [self.visible_sprites], self.obstacle_sprites)       

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class CameraGroup(pygame.sprite.Group):
    """
    Manage the movement of the map in relation to the player. 
    Show different objects sorted by their Y position.
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

        self.floor_surf = pygame.image.load("assets/map/level_0.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_position)

        #sort the drawing order by the y coordinate of the object/player
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
