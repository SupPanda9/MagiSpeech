import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    # special is a variable used for the value of the next level, as well as other specific dynamics
    def __init__(self, position, groups, sprite_type, special, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface

        if self.sprite_type == "map_transition":
            self.next_map = special

        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - TILESIZE))
        elif sprite_type == "treasure":
            self.rect = self.image.get_rect(topleft = position)
            self.rect = self.rect.inflate((15,15))
        else:
            self.rect = self.image.get_rect(topleft = position)

        self.hitbox = self.rect.inflate(0, -10)