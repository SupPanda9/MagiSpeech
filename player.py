import pygame
from settings import *
from helpers import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack):
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

        self.attacking = False
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites
        self.cooldown = {
            "attack" : 300,
            "invincibility" : 500
        }

        self.stats = player_stats
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 0
        self.speed = self.stats["speed"]
        
        player_max_stats = {"health" : 100, "energy" : 60, "attack" : 10, "magic" : 4, "speed" : 5}
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.vulnerable = True
        self.hit_time = None

    def input(self):
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

            # make the voice logic later
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.cooldown["attack"] +  weapon_data["sword"]["cooldown"]:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.cooldown["invincibility"]:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data["sword"]["damage"]
        return base_damage + weapon_damage

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self):
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
        self.rect.topleft = position
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

        self.hitbox = self.rect.inflate(-2, -26)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
