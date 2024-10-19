import pygame.sprite

from settings import *

class CameraRange(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.set_alpha(120)
        self.image.fill('#FFFF8F')
        self.rect = self.image.get_rect(topleft = pos)
