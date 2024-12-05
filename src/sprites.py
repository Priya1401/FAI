# from settings import *

# class Sprite(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)

# class CollisionSprite(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, obj):
#         super().__init__(groups)
#         self.image = surf
#         self.image = pygame.transform.scale(self.image, (int(obj.width), int(obj.height)))
#         self.rect = self.image.get_rect(topleft=pos)

#         # if hasattr(obj, 'rotation') and obj.rotation != 0:
#         #     original_center= self.rect.center
#         #     self.image = pygame.transform.rotate(self.image, -obj.rotation)
#         #     self.rect = self.image.get_rect()  # Get the new rect after rotation
#         #     # self.rect.center =original_center
#         #
#         #
#         #
#         #     self.rect = self.image.get_rect(center=original_center)
#         # self.rect.size = obj.size


import pygame.sprite
from pygame.surface import Surface
from pygame.sprite import Group


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: Surface, groups: Group):
        """ Initializes the sprite with a position, surface, and groups. """
        super().__init__(groups)
        if not isinstance(surf, Surface):
            raise ValueError("surf must be a valid pygame.Surface")
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: Surface, groups: Group, obj: object):
        """
        Initializes a collision sprite with a position, surface, groups, and an object.
        Scales the image based on the object's width and height.
        """
        super().__init__(groups)
        if not isinstance(surf, Surface):
            raise ValueError("surf must be a valid pygame.Surface")

        # Scale the image to match the object's dimensions
        self.image = surf
        self.image = pygame.transform.scale(self.image, (int(obj.width), int(obj.height)))
        self.rect = self.image.get_rect(topleft=pos)
