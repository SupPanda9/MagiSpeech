import pygame
from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/player/down/down_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.orientation = "down"
        self.hitbox = self.rect.inflate(-2, -26)

        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
    

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input
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

    def update(self):
        self.input()
        self.move(self.speed)
