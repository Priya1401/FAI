import pygame.time
from pygame.display import update

from thief import Thief
from guard import Guard
from cashbag import Cashbag
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
        self.cashbag = pygame.sprite.Group()

        self.setup()

        # sprites
        self.thief = Thief((400,300), self.all_sprites, self.collision_sprites)
        self.guard = Guard((600,350), self.all_sprites, self.collision_sprites)

    def setup(self):
        map = load_pygame(join('src','maps','level1_map.tmx'))
        for x,y, image in map.get_layer_by_name('Floor').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Object'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites), obj)

        # Place a single cash bag at a fixed position
        cash_bag_position = (700, 700)  # Fixed coordinates (adjust as needed)
        Cashbag(cash_bag_position, (self.all_sprites, self.cashbag)) 

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

            # # Check if thief collected the cash bag
            # for cashbag in self.cashbag:
            #     cashbag.update(self.thief.rect)  # Passing thief's rect for collision detection

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()


        pygame.quit()

if __name__ =='__main__':
    game = Game()
    game.run()