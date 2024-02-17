import pygame
from settings import *
from helpers import import_folder
from entity import Entity

class Player(Entity):
    """
    Represents the player character in the game.

    Attributes:
    - image: The current image of the player character.
    - rect: The rectangle representing the player's position and size.
    - hitbox: The smaller hitbox representing the player's collision area.
    - position: The current position of the player.
    - status: The current status of the player character (e.g., movement 
    direction or attacking).
    - create_magic: A function to create magic attack.
    - magic_index: The index of the current magic ability.
    - magic: The name of the current magic ability.
    - can_switch_magic: A boolean indicating whether the player can switch magic abilities.
    - magic_switch_time: The time at which the player switched magic abilities.
    - attacking: A boolean indicating whether the player is currently performing an attack.
    - attack_time: The time at which the player initiated the attack.
    - obstacle_sprites: The sprite group representing obstacle sprites in the game.
    - cooldown: A dictionary containing cooldown times for various actions.
    - stats: A dictionary containing the player's statistics (e.g., health, energy, attack).
    - health: The current health points of the player.
    - energy: The current energy points of the player.
    - exp: The experience points of the player.
    - speed: The movement speed of the player.
    - create_attack: A function to create physical attack.
    - destroy_attack: A function to destroy physical attack.
    - vulnerable: A boolean indicating whether the player is currently vulnerable to damage.
    - hurt_time: The time at which the player was last damaged and became invincible.
    - animations: A dictionary containing animation frames for player actions and directions.
    - frame_index: The index of the current animation frame.
    - animation_speed: The speed at which the animation frames are played.

    Methods:
    - input(): Handle player input for movement and actions.
    - import_player_assets(): Load player animations from files.
    - cooldowns(): Manage cooldowns for player actions.
    - get_full_weapon_damage(): Calculate the total damage including the player's attack and weapon damage.
    - get_full_magic_damage(): Calculate the total damage including the player's magic strength.
    - energy_recovery(): Handle energy recovery over time.
    - animate(): Update the player's animation based on current status and direction.
    - get_status(): Determine the current status of the player based on movement and actions.
    - move_to(): Move the player character to a specified position.
    - update(): Update the player's state and behavior.
    """
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        """
        Initialize the Player object with the given position and attributes.

        Parameters:
        - position: The initial position of the player character.
        - groups: The sprite groups to which the player belongs.
        - obstacle_sprites: The sprite group representing obstacle sprites in the game.
        - create_attack: A function to create physical attacks.
        - destroy_attack: A function to destroy physical attacks.
        - create_magic: A function to create magical effects.
        """
        super().__init__(groups)
        self.image = pygame.image.load('assets/player/down/down_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        
        # the hitbox is smaller than the rectangle to create illusion of depth by showing
        # small part of the player above objects, and allow him to move easier in one tile
        # sized spaces
        self.hitbox = self.rect.inflate(-2, -26)
        self.position = position

        self.import_player_assets()
        self.status = "down"

        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.attacking = False
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites
        self.cooldown = {
            "attack" : 300,
            "invincibility" : 500,
            "switch_magic" : 200
        }

        self.stats = player_stats
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 0
        self.speed = self.stats["speed"]
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.vulnerable = True
        self.hurt_time = None

    def input(self):
        """Handle player input for movement and actions."""
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_w]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]                
                self.create_magic(style, strength, cost)
            
            if keys[pygame.K_q] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def import_player_assets(self):
        """Load player animations from files."""
        character_path = "assets/player/"
        self.animations = {
            "up" : [],
            "down" : [],
            "left" : [],
            "right" : [],
            "up_idle" : [],
            "down_idle" : [],
            "left_idle" : [],
            "right_idle" : [],
            "up_attack" : [],
            "down_attack" : [],
            "left_attack" : [],
            "right_attack" : []
        }
        # the directories are named after the specific movement
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def cooldowns(self):
        """Manage cooldowns for player actions."""
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.cooldown["attack"] +  weapon_data["sword"]["cooldown"]:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.cooldown["switch_magic"]:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.cooldown["invincibility"]:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        """
        Calculate the total damage including the player's attack and weapon damage.
        
        Returns:
        - The total damage value.
        """
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data["sword"]["damage"]
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        """
        Calculate the total damage including the player's magic strength.
        
        Returns:
        - The total damage value.
        """
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage
    
    def energy_recovery(self):
        """Handle energy recovery over time."""
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def animate(self):
        """
        Updates the player's animation based on current 
        status and direction.
        """
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self):
        """
        Determine the current status of the player
        based on movement and actions.
        """
        if self.direction.x == 0 and self.direction.y == 0 and not "attack" in self.status:
            if not "idle" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move_to(self, position):
        """
        Move the player character to a specified position.
        
        Parameters:
        - position: The target position for the player.
        """
        self.rect.topleft = position
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

        self.hitbox = self.rect.inflate(-2, -26)

    def update(self):
        """Update the player's state and behavior."""
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()