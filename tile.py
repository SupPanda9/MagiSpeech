import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile sprite used in the game map.

    Parameters:
    - position: The position of the tile on the game map.
    - groups: The sprite groups to which the tile belongs.
    - sprite_type: Type of the tile sprite.
    - special: Special value associated with the tile, used for map
    transitions, treasure opening and other dynamics.
    - surface: Surface representing the appearance of the tile. 
    Defaults to pygame.Surface((TILESIZE,TILESIZE)).

    Attributes:
    - sprite_type: Type of the tile sprite.
    - image: Image surface representing the tile.
    - rect: Rectangle defining the position and size
    of the tile sprite.
    - hitbox: Rectangle defining the collidable hitbox of the 
    tile sprite.

    Note:
    For 'map_transition' tiles, the special value represents the next map.
    For 'treasure' tiles, the special value represents the type of chest 
    used for opening the open treasure image.
    """
    # special is a variable used for the value of the next level, as well as other specific dynamics
    def __init__(self, position, groups, sprite_type, special, surface = pygame.Surface((TILESIZE,TILESIZE))):
        """
        Initialize the Tile sprite. 
        """
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
            self.type_of_chest = special
        else:
            self.rect = self.image.get_rect(topleft = position)

        self.hitbox = self.rect.inflate(0, -10)