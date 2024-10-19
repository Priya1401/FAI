import pygame.sprite

from settings import *

class GuardRange(pygame.sprite.Sprite):

    def __init__(self, pos, length, breadth, groups, collision_sprites):
        super().__init__(groups)
        self.width = breadth
        self.height = length
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_alpha(100)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = pos)

        self.half_rect = pygame.Rect(0, 0, self.width, self.height // 2)
        pygame.draw.rect(self.image, 'Red', self.half_rect)

        # movements
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        # self.movement = None


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # if not self.direction.y == 0:
        #     self.movement = "down" if self.direction.y > 0 else "up"
        # if not self.direction.x==0:
        #     self.movement = "right" if self.direction.x > 0 else "left"
        self.direction = self.direction.normalize() if self.direction else self.direction


    def move(self, dt):
        # if self.movement=="up" or self.movement=="down":
        #     self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # elif self.movement=="left" or self.movement=="right":
        #     self.image = pygame.transform.scale(self.image, (self.height, self.width))
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

    def update(self, dt):
        self.input()
        self.move(dt)