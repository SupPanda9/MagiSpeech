import pygame
from helpers import import_folder
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
			"flame": import_folder("assets/particles/flame/frames"),
			"aura": import_folder("assets/particles/aura"),
			"heal": import_folder("assets/particles/heal/frames"),
			}

    def create_particles(self, animation_type, position, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(position, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()