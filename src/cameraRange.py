import pygame.sprite

from settings import *


class CameraRange(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        self.draw_cone(pos, size)
        self.rect = self.image.get_rect(topleft=pos)

    def draw_cone(self, pos, size):
        # Calculate the points for the cone shape
        point1 = (size[0], 15)  # Top point (tip of the cone)
        point2 = (size[1] // 100 , 0)  # Bottom left point
        point3 = (size[1] // 100, size[1])  # Bottom right point

        # Draw the cone shape
        pygame.draw.polygon(self.image, (255, 255, 143, 150), [point1, point2, point3])  # Yellow with alpha
        self.image.set_colorkey((0, 0, 0))  # Set black as transparent if you want the background to show through

# Example usage:
# camera_range = CameraRange((100, 100), (200, 100), groups)