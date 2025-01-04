### MODULE IMPORTS ###

import pygame
from math import atan2, degrees
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from os.path import join

### Gun CLASS ###

class Gun(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, player, group):

        # Main variables
        self.all_sprites = group[0]
        self.bullet_sprites = group[1]
        super().__init__(self.all_sprites)
        self.player = player
        self.distance = 200
        self.direction = pygame.math.Vector2(1,0)
        self.og = pygame.image.load(join('..', 'images', 'gun', 'gun.png'))
        self.image = self.og
        self.rect = self.image.get_frect(center = self.player.rect.center + self.direction * self.distance)
        self.cooldown = 10
        self.can_shoot = True
        self.previous_shot = 0
        self.bullet_surf = pygame.image.load(join('..', 'images', 'gun', 'bullet.png')).convert_alpha()

        # Audio
        self.shot_sound = pygame.mixer.Sound(join('..', 'audio', 'shoot.wav'))
        self.shot_sound.set_volume(0.2)

    # Get unit vector in the direction from player to mouse.
    def get_direction(self):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.math.Vector2((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = (mouse_pos - player_pos).normalize()

    # Rotate gun based on mouse position.
    def rotate_gun(self):
        angle = degrees(atan2(self.direction.x, self.direction.y)) - 90
        if self.direction.x > 0:
            self.image = pygame.transform.rotozoom(self.og, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.og, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_frect(center = self.rect.center)

    # Shoot bullets.
    def shoot(self):
        if pygame.time.get_ticks() - self.previous_shot >= 600:
            self.can_shoot = True
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.rect.center + self.direction * 50
            Bullet(self.bullet_surf, pos, self.direction, (self.all_sprites, self.bullet_sprites))
            self.shot_sound.play()
            self.can_shoot = False
            self.previous_shot = pygame.time.get_ticks()

    # Update fn for this sprite.
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.direction * self.distance 
        self.shoot()

### Bullet CLASS ###

class Bullet(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, surf, pos, direction, group):
        super().__init__(group)
        self.direction = direction
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.speed = 800
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    # Update fn for this sprite.
    def update(self, dt):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rect.center += self.direction * self.speed * dt

### END ###
