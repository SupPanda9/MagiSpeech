import pygame

class Entity(pygame.sprite.Sprite):
    """
    Base class for game entities such as players and enemies.

    Parameters:
    - groups: The sprite groups to which the entity belongs.

    Attributes:
    - frame_index: Index representing the current frame in the entity's animation.
    - animation_speed: Speed at which the entity's animation cycles through frames.
    - direction: Vector representing the entity's movement direction.

    Methods:
    - move(speed): Move the entity in the current direction with the specified speed.
    - collision(direction): Handle collision detection and response in the specified direction.
    """
    def __init__(self, groups):
        """Initialize the entity with the given groups."""
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """
        Move the entity in the current direction with the specified speed.

        Parameters:
        - speed(float): The speed at which the entity should move.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        Handle collision detection and response in the specified direction.

        Parameters:
        - direction(str): The direction of collision detection and response ("horizontal" or "vertical").
        """
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top 
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom