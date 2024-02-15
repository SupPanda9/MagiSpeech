import pygame
from settings import *
from tile import Tile
from player import Player
from helpers import *
from weapon import Weapon


class World:
    def __init__(self):
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

    def change_map(self, map_number):
        self.player.remove(self.level.visible_sprites)
        del self.level
        self.changed_map = True

        self.level = Level(map_number, self)

        self.changed_map = False
        
        self.player.move_to(self.position)

        self.player.obstacle_sprites = self.level.obstacle_sprites
        self.player.add(self.level.visible_sprites)

    def create_physical_attack(self):
        self.current_attack = Weapon(self.player, [self.level.visible_sprites, self.level.attack_sprites])

    def destroy_physical_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


class Level:
    def __init__(self, map_number, world):
        # groups of sprites with different behavior
        self.map_number = map_number
        self.visible_sprites = CameraGroup(self.map_number)
        self.obstacle_sprites = pygame.sprite.Group()
        self.map_transition_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()

        self.world = world
        self.create_map()

    def create_map(self):
        layouts = {
            "boundary" : import_csv_layout(f"assets/map/level_{self.map_number}_FloorBlocks.csv"),
            "map_transition" : import_csv_layout(f"assets/map/level_{self.map_number}_MapTransition.csv"),
            "object": import_csv_layout(f"assets/map/level_{self.map_number}_Objects.csv"),
            "entities" : import_csv_layout(f"assets/map/level_{self.map_number}_Entities.csv")
        }
        graphics = {
            "objects" : import_folder("assets/objects")
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

    def check_map_transition(self):
        for sprite in self.map_transition_sprites:
            if pygame.sprite.collide_rect(self.world.player, sprite):
            # Get the next level and the next position from the sprite's attributes
                next_map = sprite.next_map
                self.world.from_map = self.map_number
                # Call the change_map method with those parameters
                self.world.change_map(next_map)

    def run(self): 
        self.visible_sprites.custom_draw(self.world.player)
        self.visible_sprites.update()
        self.check_map_transition()


class CameraGroup(pygame.sprite.Group):
    """
    Manage the movement of the map in relation to the player. 
    Show different objects sorted by their Y position.
    """
    def __init__(self, level):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

        self.floor_surf = pygame.image.load(f"assets/map/level_{level}.png").convert()
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
