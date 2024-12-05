import pygame.sprite

from settings import *

class CameraRange(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        self.image = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        self.draw_cone(pos, size)
        self.rect = self.image.get_rect(topleft=pos)

        # Create a mask only for the non-transparent area
        opaque_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                color = self.image.get_at((x, y))
                if color[3] > 128:  # Only add pixels with alpha > 128
                    opaque_surface.set_at((x, y), (255, 255, 143))  # Same color without transparency

        # Generate the mask from the opaque-only surface
        self.mask = pygame.mask.from_surface(opaque_surface)

    def draw_cone(self, pos, size):
        # Calculate the points for the cone shape
        point1 = (size[0], 15)  # Top point (tip of the cone)
        point2 = (size[1] // 100, 0)  # Bottom left point
        point3 = (size[1] // 100, size[1])  # Bottom right point

        # Draw the cone shape
        pygame.draw.polygon(self.image, (255, 255, 143, 150), [point1, point2, point3])  # Yellow with alpha
        # Set black as transparent for display purposes only
        self.image.set_colorkey((0, 0, 0))
