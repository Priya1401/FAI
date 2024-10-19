import pygame.sprite

from settings import *

class securityCamera(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('src', 'images', 'camera-2.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
