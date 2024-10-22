import pygame.sprite

from settings import *

class Thief(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('src','images','thief_test.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction


    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        if self.rect.x > WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > WINDOW_HEIGHT-50:
            self.rect.y = WINDOW_HEIGHT-50
        if self.rect.y < 0:
            self.rect.y = 0



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