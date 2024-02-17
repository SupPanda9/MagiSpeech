import pygame

class Weapon(pygame.sprite.Sprite):
    """
    Class representing a weapon sprite used by the player.

    Parameters:
    - player: The player object associated with the weapon.
    - groups: The sprite groups to which the weapon belongs.

    Attributes:
    - sprite_type: Type of this sprite (weapon).
    - image: Image surface representing the weapon.
    - rect: Rectangle defining the position and size of the weapon sprite.

    Note:
    The weapon sprite's position is determined based on the player's
    direction.
    """
    def __init__(self, player, groups):
        """Initialize the weapon with the given groups."""
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]

        full_path = f"assets/sword/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()
        
        if direction == "right":
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.Vector2(0,16))
        elif direction == "left":
             self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.Vector2(0,16))
        elif direction == "down":
             self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.Vector2(-10, 0))