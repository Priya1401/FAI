import pygame

class GuardRange(pygame.sprite.Sprite):
    def __init__(self, pos, length, breadth, groups, collision_sprites, guard):
        super().__init__(groups)
        self.guard = guard
        self.width = breadth
        self.height = length
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_alpha(100)
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

        self.half_rect = pygame.Rect(0, 0, self.width, self.height // 2)
        pygame.draw.rect(self.image, 'Red', self.half_rect)

        # Movement properties
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        self.handle_collision()

    def handle_collision(self):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)
