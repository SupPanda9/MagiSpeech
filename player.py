import pygame
from settings import *
from helpers import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/player/down/down_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        
        # the hitbox is smaller than the rectangle to create illusion of depth by showing
        # small part of the player above objects, and allow him to move easier in one tile
        #  
        self.hitbox = self.rect.inflate(-2, -26)

        
        self.import_player_assets()
        print(self.animations)
        self.orientation = "down"

        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
    

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.orientation = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.orientation = "down"
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.orientation = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.orientation = "left"
        else:
            self.direction.x = 0

    def import_player_assets(self):
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

    def animate(self):
        animation = self.animations[self.orientation]
        self.frame_index += self.animation_speed


        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_orientation(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.orientation:
                self.orientation = self.orientation + "_idle"

    def update(self):
        self.input()
        self.get_orientation()
        self.animate()
        self.move(self.speed)
