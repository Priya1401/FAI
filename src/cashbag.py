import pygame.sprite

from settings import *

class Cashbag(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('src', 'images', 'cashbag.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        # self.collected = False

    # def collect(self, thief_rect):
    #     if self.rect.colliderect(thief_rect):  # Ensure that thief_rect is a valid pygame.Rect
    #         self.collected = True  # Mark the bag as collected
    #         self.kill()  # Remove the cash bag sprite from the game

    # def update(self, thief_rect):
    #     self.collect(thief_rect)  # Check if the thief has collected the cash bag
