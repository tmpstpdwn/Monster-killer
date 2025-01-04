### MODULE IMPORTS ###

import pygame
from random import randint
from os.path import join, basename 
from os import walk

### Player CLASS ###

class Player(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, pos, group, collition_sprites):
        super().__init__(group)
        self.load_frames()
        self.walk_dir = 'left'
        self.current_index = 0
        self.image = self.frames[self.walk_dir][self.current_index]
        self.rect = self.image.get_frect(center = pos)
        self.rrect = self.rect.inflate(-60, -90)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 600
        self.collition_sprites = collition_sprites
        self.animation_speed = 0

    # Load player frames for animation.
    def load_frames(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for folder_path, sub_folders, files in walk(join('..', 'images', 'player')):
            if files:
                for file in sorted(files, key=lambda x: int(x.split('.')[0])):
                    file_path = join(folder_path, file)

                    surf = pygame.image.load(file_path).convert_alpha()
                    key = basename(folder_path)
                    self.frames[key].append(surf)

    # Get input and set direction.
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        if not self.animation_speed:
            self.animation_speed = 125
        if self.direction.x > 0:
            self.walk_dir = 'right'
        elif self.direction.x < 0:
            self.walk_dir = 'left'
        elif self.direction.y > 0:
            self.walk_dir = 'down'
        elif self.direction.y < 0:
            self.walk_dir = 'up'
        else:
            self.animation_speed = 0

    # Set the player in motion based on its updated direction.
    def movement(self, dt):
        self.rrect.centerx += self.direction.x * self.speed * dt
        self.collition('Horizontal')
        self.rrect.centery += self.direction.y * self.speed * dt
        self.collition('Vertical')
        self.rect.center = self.rrect.center
    
    # Check for collisions.
    def collition(self, direction):
        for sprite in self.collition_sprites:
            if sprite.rect.colliderect(self.rrect):
                if direction == "Horizontal":
                    if self.direction.x > 0: self.rrect.right = sprite.rect.left
                    if self.direction.x < 0: self.rrect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rrect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rrect.top = sprite.rect.bottom

    # Animate the player using loaded frames.
    def animate(self, dt):
        self.current_index += 0.1 * self.animation_speed * dt
        if self.current_index >= len(self.frames[self.walk_dir]): self.current_index = 0
        self.image = self.frames[self.walk_dir][int(self.current_index)]
        self.rect = self.image.get_frect(center = self.rect.center)
        self.rrect = self.rect.inflate(-60, -90)

    # Update the player.
    def update(self, dt):
        self.input()
        self.animate(dt)
        self.movement(dt)

### Enemy ClASS ###

class Enemy(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, frames, pos, player, group, collition_sprites):
        super().__init__(group)
        self.frames = frames
        self.current_index = 0
        self.player = player
        self.collition_sprites = collition_sprites
        self.image = self.frames[self.current_index]
        self.rect = self.image.get_frect(center = pos)
        self.rrect = self.rect.inflate(-60, -90)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = randint(200, 300)
        self.death_time = 0
        self.death_duration = 400

    # Update the enemy direction based on player position.
    def update_direction(self):
        self.direction.update((self.player.rect.x - self.rect.x), (self.player.rect.y - self.rect.y))
        self.direction = self.direction.normalize() if self.direction else self.direction

    # Move the enemy based on updated direction.
    def movement(self, dt):
        self.rrect.centerx += self.direction.x * self.speed * dt
        self.collition("Horizontal")
        self.rrect.centery += self.direction.y * self.speed * dt
        self.collition("Vertical")
        self.rect.center = self.rrect.center

    # Check for collisions.
    def collition(self, direction):
        for sprite in self.collition_sprites:
            if sprite.rect.colliderect(self.rrect):
                if direction == "Horizontal":
                    if self.direction.x > 0: self.rrect.right = sprite.rect.left
                    if self.direction.x < 0: self.rrect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rrect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rrect.top = sprite.rect.bottom

    # Animate enemy using loaded frames.
    def animate(self):
        self.current_index += 0.1
        if self.current_index < len(self.frames):
            self.image = self.frames[int(self.current_index)]
            self.rect = self.image.get_frect(center = self.rect.center)
        else:
            self.current_index = 0

    # Set the death timer and change the enemy image.
    def end(self):
        self.death_time = pygame.time.get_ticks()
        surf = self.mask.to_surface()
        surf.set_colorkey('black')
        self.image = surf

    # Timer for death after hit.
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    # Update enemy.
    def update(self, dt):
        if self.death_time == 0:
            self.update_direction()
            self.animate()
            self.movement(dt)
        else:
            self.death_timer()

### END ###
