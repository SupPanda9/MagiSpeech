import pygame
from settings import *
from entity import Entity
from helpers import *

class Enemy(Entity):
    """
    Represent an enemy character in the game world.

    Attributes:
    - sprite_type: A string representing the type of sprite (in this case, 
    "enemy").
    - status: A string representing the current status of the enemy (e.g.,
    "idle", "move", "attack").
    - image: A Pygame surface representing the current image of the enemy.
    - rect: A Pygame rect representing the position and size of the enemy's
    image.
    - hitbox: A Pygame rect representing the hitbox of the enemy for
    collision detection.
    - obstacle_sprites: A Pygame sprite group representing obstacle sprites
    in the level.
    - enemy_name: A string representing the name of the enemy character.
    - health: An integer representing the current health points of the enemy.
    - exp: An integer representing the experience points granted to the
    player upon defeating the enemy.
    - speed: An integer representing the movement speed of the enemy.
    - attack_damage: An integer representing the damage inflicted by the
    enemy's attacks.
    - resistance: An integer representing the resistance of the enemy to
    damage.
    - attack_radius: An integer representing the radius within which the
    enemy can perform attacks.
    - notice_radius: An integer representing the radius within which the
    enemy notices the player.
    - attack_type: A string representing the type of attack performed by
    the enemy.
    - can_attack: A boolean indicating whether the enemy can perform an
    attack.
    - attack_time: An integer representing the time of the last attack
    performed by the enemy.
    - attack_cooldown: An integer representing the cooldown period
    between attacks.
    - damage_player: A function reference to damage the player character.
    - add_xp: A function reference to add experience points to the player 
    character.
    - vulnerable: A boolean indicating whether the enemy is currently
    vulnerable to damage.
    - hit_time: An integer representing the time of the last hit received
    by the enemy.
    - invincibility_duration: An integer representing the duration of
    invincibility after being hit.

    Methods:
    - __init__(self, name, position, groups, obstacle_sprites, 
                damage_player, add_xp): 
    Initialize an enemy instance with the given attributes.
    - import_graphics(self, name): Load enemy graphics/animations from files.
    - get_player_distance_direction(self, player): Calculate the distance and
    direction vector from the enemy to the player.
    - get_status(self, player): Determine the status of the enemy based on the
    player's position.
    - actions(self, player): Perform actions based on the enemy's status.
    - animate(self): Animate the enemy based on its current status.
    - cooldowns(self): Manage cooldowns for the enemy's actions.
    - get_damage(self, player, attack_type): Inflict damage on the enemy.
    - check_death(self): Check if the enemy has been defeated.
    - hit_reaction(self): Handle the reaction of the enemy when hit.
    - update(self): Update the enemy's state and behavior.
    - enemy_update(self, player): Update the enemy's behavior based on the
    player's position.
    """
    def __init__(self, name, position, groups, obstacle_sprites, damage_player, add_xp):
        """Initialize an enemy instance."""
        super().__init__(groups)
        self.sprite_type = "enemy"

        self.import_graphics(name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        self.enemy_name = name
        enemy_info = enemies_data[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        self.add_xp = add_xp

    def import_graphics(self, name):
        """
        Load enemy graphics/animations from files.

        Parameters:
        - name: String representing the name of the enemy.
        """
        self.animations = {
            "idle" : [], 
            "move" : [], 
            "attack" : [],
        }
        main_path = f"assets/enemies/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        """
        Calculate the distance and direction vector from the enemy to 
        the player.

        Parameters:
        - player: Instance of the Player class representing the player
        character.

        Returns:
        - Tuple containing the distance and direction vector.
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        """
        Determine the status of the enemy based on the player's position.

        Parameters:
        - player: Instance of the Player class representing the player
        character.
        """
        distance = self.get_player_distance_direction(player)[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        """
        Perform actions based on the enemy's status.

        Parameters:
        - player: Instance of the Player class representing the player
        character.
        """
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        """Animate the enemy based on its current status."""
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldowns(self):
        """Manage cooldowns for the enemy's actions."""
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        """
        Inflict damage on the enemy.

        Parameters:
        - player: Instance of the Player class representing the player character.
        - attack_type: String representing the type of attack.
        """
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def check_death(self):
        """Check if the enemy has been defeated."""
        if self.health <= 0:
            self.kill()
            self.add_xp(self.exp)

    def hit_reaction(self):
        """Handle the reaction of the enemy when hit."""
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        """Update the enemy's state and behavior."""
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        """
        Update the enemy's behavior based on the player's position.

        Parameters:
        - player: Instance of the Player class representing the player
        character.
        """
        self.get_status(player)
        self.actions(player)