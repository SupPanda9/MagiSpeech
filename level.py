import pygame
from settings import *
from tile import Tile
from player import Player
from helpers import *
from weapon import Weapon
from enemy import Enemy
from minigame import MiniGame
from hud import HUD

class World:
    """
    Represent the game world, containing the current level, player, and game state.

    Attributes:
    - display_surface: Pygame surface representing the display window.
    - position: Tuple representing the current position of the player in the world.
    - from_map: Integer representing the index of the previous map.
    - changed_map: Boolean indicating whether the map has been changed.
    - level: Instance of the Level class representing the current game level.
    - current_attack: Current attack instance being used by the player.
    - player: Instance of the Player class, representing the player character.
    - current_mini_game: Instance of the MiniGame class representing the current mini-game being played.
    - mini_game_active: Boolean indicating whether a mini-game is currently active.
    - solved_mini_game: Boolean indicating whether the current mini-game has been solved correctly.
    - game_correct_answers: Integer representing the number of correct answers in the current mini-game.
    """
    def __init__(self):
        """
        Initialize the World object by setting up the display surface, position, level, player, and game state.
        """
        self.display_surface = pygame.display.get_surface()

        self.position = (0,0)
        self.from_map = 0
        self.changed_map = False
        self.level = Level(0, self)

        self.current_attack = None

        self.player = Player(self.position, 
                            [self.level.visible_sprites], 
                            self.level.obstacle_sprites,
                            self.create_physical_attack,
                            self.destroy_physical_attack)
        
        self.current_mini_game = None
        self.mini_game_active = False
        self.solved_mini_game = False
        self.game_correct_answers = 0

    def change_map(self, map_number):
        """
        Changes the current map to the specified map number.

        Parameters:
        - map_number: Integer representing the index of the next map.
        """
        self.player.remove(self.level.visible_sprites)
        del self.level
        self.changed_map = True

        self.level = Level(map_number, self)

        self.changed_map = False
        
        self.player.move_to(self.position)

        self.player.obstacle_sprites = self.level.obstacle_sprites
        self.player.add(self.level.visible_sprites)

    def create_physical_attack(self):
        """Create a physical attack instance for the player."""
        self.current_attack = Weapon(self.player, [self.level.visible_sprites, self.level.damaging_sprites])

    def destroy_physical_attack(self):
        """Destroy the current physical attack instance."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def start_mini_game(self):
        """Start a mini-game if the player is interacting with a treasure."""
        for treasure in self.level.treasure_sprites:
            if self.player.rect.colliderect(treasure.rect):
                self.mini_game_active = True
                # choose which mini game to start
                self.current_mini_game = MiniGame(self)
                self.level.treasure_sprites.remove(treasure)

                graphics = {
                    "treasures" : import_folder("assets/treasure")
                }

                if treasure.type_of_chest == 0:
                    treasure.image = graphics["treasures"][2]
                else:
                    treasure.image = graphics["treasures"][3]

                # create the image of the opened chest of the corresponding type
                break
    
    def add_xp(self, value):
        """
        Add experience points to the player.
        
        Parameters:
        - value: Integer representing the amount of experience points to add.
        """
        self.player.exp += value

class Level:
    """
    Represent a game level, containing the map layout, sprites, and game logic.
    
    Attributes:
    - map_number: Integer representing the index of the level map.
    - visible_sprites: Instance of CameraGroup representing visible sprites in the level.
    - obstacle_sprites: Pygame sprite group representing obstacle sprites in the level.
    - map_transition_sprites: Pygame sprite group representing map transition sprites in the level.
    - damaging_sprites: Pygame sprite group representing damaging sprites in the level.
    - damageable_sprites: Pygame sprite group representing damageable sprites in the level.
    - treasure_sprites: Pygame sprite group representing treasure sprites in the level.
    - world: Instance of the World class representing the game world.
    - hud: Instance of the HUD class representing the user interface.
    """
    def __init__(self, map_number, world):
        """
        Initialize the Level object with the specified map number and game world.

        Parameters:
        - map_number: Integer representing the index of the level map.
        - world: Instance of the World class representing the game world.
        """
        # groups of sprites with different behavior
        self.map_number = map_number
        self.visible_sprites = CameraGroup(self.map_number)
        self.obstacle_sprites = pygame.sprite.Group()
        self.map_transition_sprites = pygame.sprite.Group()

        self.damaging_sprites = pygame.sprite.Group()
        self.damageable_sprites = pygame.sprite.Group()
        self.treasure_sprites = pygame.sprite.Group()

        self.world = world
        self.create_map()
        self.hud = HUD()

    def create_map(self):
        """
        Create the game map by loading layout data and generating sprites, based on CSVs.
        """
        layouts = {
            "boundary" : import_csv_layout(f"assets/map/level_{self.map_number}_FloorBlocks.csv"),
            "map_transition" : import_csv_layout(f"assets/map/level_{self.map_number}_MapTransition.csv"),
            "object": import_csv_layout(f"assets/map/level_{self.map_number}_Objects.csv"),
            "entities" : import_csv_layout(f"assets/map/level_{self.map_number}_Entities.csv"),
            "treasures" : import_csv_layout(f"assets/map/level_{self.map_number}_Treasures.csv")
        }
        graphics = {
            "objects" : import_folder("assets/objects"),
            "treasures" : import_folder("assets/treasure")
        }

        for style, layout in layouts.items():       
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if style == "boundary":
                            Tile((x,y), [self.obstacle_sprites], "invisible", None)
                        
                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "object", None, surf)

                        if style == "treasures":
                            surf = graphics["treasures"][int(col)]
                            if col == "0":
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.treasure_sprites], "treasure", 0, surf)
                            else:
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.treasure_sprites], "treasure", 1, surf)
                        
                        if style == "map_transition":
                            Tile((x,y), [self.map_transition_sprites], "map_transition", col)
                            
                            if self.world.changed_map and col == str(self.world.from_map):
                                if x == 0:
                                    self.world.position = (x + TILESIZE + 20, y)
                                elif x + TILESIZE == self.visible_sprites.floor_surf.get_width():
                                    self.world.position = (x - TILESIZE - 20, y)
                                elif y == 0:
                                    self.world.position = (x, y + TILESIZE + 20)
                                elif y + TILESIZE == self.visible_sprites.floor_surf.get_height():
                                    self.world.position = (x, y - TILESIZE - 20)
                                else:
                                    self.world.position = (x, y + TILESIZE + 20)
                                
                        if style == "entities":
                            if not self.world.changed_map and col == "394":
                                self.world.position = (x,y)
                            elif col != "394":
                                if col == "390" : 
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                elif col == "393":
                                    monster_name = "squid"
                                Enemy(monster_name, 
                                    (x,y), 
                                    [self.visible_sprites, 
                                    self.damageable_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.world.add_xp)

    def check_map_transition(self):
        """
        Check for collisions between the player and map transition 
        sprites to change the current level.
        """
        for sprite in self.map_transition_sprites:
            if pygame.sprite.collide_rect(self.world.player, sprite):
            # Get the next level and the next position from the sprite's attributes
                next_map = sprite.next_map
                self.world.from_map = self.map_number
                # Call the change_map method with those parameters
                self.world.change_map(next_map)

    def player_attack(self):
        """Handle player attacks logic and damage to other sprites."""
        if self.damaging_sprites:
            for damaging_sprite in self.damaging_sprites:
                collision_sprites = pygame.sprite.spritecollide(damaging_sprite, self.damageable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.world.player, damaging_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        """
        Damage the player by the specified amount and set the player as 
        invulnerable for a brief period.

        Parameters:
        - amount: Integer representing the amount of damage.
        - attack_type: String representing the type of attack.
        """
        if self.world.player.vulnerable:
            self.world.player.health -= amount
            print(f"{self.world.player.health}")
            self.world.player.vulnerable = False
            self.world.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        """
        Run the game logic for the current level, including updating sprites, 
        handling interactions, and checking for level transitions.
        """
        self.visible_sprites.custom_draw(self.world.player)
        self.visible_sprites.update()
        self.ui.display(self.world.player)
        
        if self.world.mini_game_active:
            self.world.solved_mini_game_exp = 0
            self.world.current_mini_game.run()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.world.mini_game_active = False
        else:
            self.visible_sprites.enemy_update(self.world.player)
            self.player_attack()
            self.check_map_transition()
            self.check_death()

    def check_death(self):
        """
        Checks if the player has died and resets their health and experience points
        and reposition him at the start of the map.
        """
        if self.world.player.health <= 0:
            self.world.player.health = self.world.player.stats["health"]
            self.world.change_map(0)
            self.world.player.exp = 0


class CameraGroup(pygame.sprite.Group):
    """
    A specialized group class for managing the game camera and drawing
    objects relative to it.

    Attributes:
        - level: The level number associated with the camera.
        - display_surface: The surface onto which objects are drawn.
        - half_width: Half the width of the display surface.
        - half_height: Half the height of the display surface.
        - offset: The camera offset vector used for alignment.
        - floor_surf: The image of the level floor.
        - floor_rect: The rect object representing the floor surface.
    """
    def __init__(self, level):
        """
        Initialize the CameraGroup with the given level number.

        Parameters:
        - level: Integer representing the level number.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

        self.floor_surf = pygame.image.load(f"assets/map/level_{level}.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        """
        Draw the visible sprites aligned to the view of the 
        player. Display objects sorted bu their Y coordinate.
        """
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_position)

        #sort the drawing order by the y coordinate of the object/player
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player):
        """Update the enemy sprites."""
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
