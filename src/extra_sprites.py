### MODULE IMPORTS ###

from settings import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
from gun_bullet import Gun

### AllSprites CLASS ### 

class AllSprites(pygame.sprite.Group):

    # Initialise necessary variables.
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(-600, -700)

    # Offset things as the player moves to simulate a camera.
    # This is a customised draw fn for this group for camera simulation.
    def draw(self, screen, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH/2) 
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT/2) 
        y_sorted = \
                sorted([i for i in self if not isinstance(i, Ground) and not isinstance(i, Gun)], key=lambda x: x.rect.centery)
        for sprite in self:
            if not isinstance(sprite, Ground): continue
            screen.blit(sprite.image, sprite.rect.topleft + self.offset)
        for sprite in y_sorted:
            screen.blit(sprite.image, sprite.rect.topleft + self.offset)
        for sprite in self:
            if not isinstance(sprite, Gun): continue
            screen.blit(sprite.image, sprite.rect.topleft + self.offset)

### CollitionSprite CLASS

class CollitionSprite(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

### Ground CLASS ###

class Ground(pygame.sprite.Sprite):

    # Initialise necessary variables.
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

### END ###
