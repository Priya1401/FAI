import pygame.sprite
import math

from settings import *

class Thief(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, guard, camera_range):
        super().__init__(groups)
        self.image = pygame.image.load(join('src','images','thief_test.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.guard = guard  # Store the guard reference
        self.camera_range = camera_range
        self.mask = pygame.mask.from_surface(self.image)

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

        # Boundary checks
        self.rect.x = max(0, min(WINDOW_WIDTH, self.rect.x))
        self.rect.y = max(0, min(WINDOW_HEIGHT - 50, self.rect.y))

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                # else:
                #     print("Gpoing through walls")
            

    def check_proximity(self):
        distance = math.hypot(self.rect.centerx - self.guard.rect.centerx, 
                              self.rect.centery - self.guard.rect.centery)
        threshold = 100  

        if distance < threshold and self.noObjectInBetween():
            print("Guard is close to the thief!")

    def noObjectInBetween(self):
        guard_pos = pygame.Vector2(self.guard.rect.center)
        thief_pos = pygame.Vector2(self.rect.center)

        for sprite in self.collision_sprites:
            if sprite.rect.clipline(guard_pos, thief_pos):
                return False  

        return True

    def check_camera_range(self):
        offset_x = self.rect.x - self.camera_range.rect.x
        offset_y =self.rect.y - self.camera_range.rect.y
        offset = (offset_x, offset_y)

        collision_point = self.camera_range.mask.overlap(self.mask, offset)
        if collision_point:
            print("Thief in camera range!")

    def update(self, dt):
        self.input()
        self.move(dt)
        self.check_proximity()
        self.check_camera_range()

