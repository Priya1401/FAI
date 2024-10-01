import pygame.time
from pygame.display import update

from thief import Thief
from guard import Guard
from sprites import *
from settings import *
from pytmx.util_pygame import load_pygame

from random import randint

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT ))
        pygame.display.set_caption("Guardians_Gambit")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites  = pygame.sprite.Group()

        self.setup()

        # sprites
        self.thief = Thief((400,300), self.all_sprites, self.collision_sprites)
        self.guard = Guard((600,300), self.all_sprites, self.collision_sprites)

    def setup(self):
        map = load_pygame(join('maps','level1_map.tmx'))
        print(map)
        # for obj in map.get_layer_by_name('Objects'):
        #     CollisionSprite((obj, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        #     print(obj.x)
        #     print(obj.y)
        #     print(obj.image)


    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()


        pygame.quit()

if __name__ =='__main__':
    game = Game()
    game.run()