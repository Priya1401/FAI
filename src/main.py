import pygame.time
from pygame.display import update

from thief import Thief
from guard import Guard
from cashbag import *
from sprites import *
from cameraRange import *
from securityCamera import *
from guardRange import *
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
        # self.blink_sprites = pygame.sprite.Group()
        
        self.cashbag_collected = False

        self.setup()

        # sprites
        x,y = (555,380)
        w,h = (180,43)
        securityCamera((765,380), self.all_sprites)
        self.camera_range = CameraRange((x,y),(w,h), self.all_sprites)
        self.guard = Guard((670,400), self.all_sprites, self.collision_sprites)
        self.thief = Thief((80,400), self.all_sprites, self.collision_sprites,self.guard)
        
        # self.guard_range = GuardRange((670,400),70,70, self.all_sprites, self.collision_sprites, self.guard)


    def setup(self):
        map = load_pygame(join('src','maps','level1_map.tmx'))
        for x,y, image in map.get_layer_by_name('Floor').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Object'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites), obj)

        # Place a single cash bag at a fixed position
        cash_bag_position = (545, 700)  # Fixed coordinates (adjust as needed)
        Cashbag(cash_bag_position, (self.all_sprites, self.cashbag))

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.cashbag_collected and pygame.sprite.spritecollide(self.thief, self.cashbag, True):
                print("Thief reached cashbag! Cashbag removed.")
                self.cashbag_collected = True
            
            if self.cashbag_collected and self.is_thief_in_terminal_area():
                print("Thief won!!!")
                self.show_winning_message("Thief won!!!")
                self.running = False
            
            if pygame.sprite.collide_rect(self.thief, self.camera_range):
                self.show_camera_alert("Thief detected by camera!")

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()


        pygame.quit()
        
    def is_thief_in_terminal_area(self):
        min_x, max_x = 320, 441
        min_y, max_y = 96, 131
        return (min_x <= self.thief.rect.x <= max_x) and (min_y <= self.thief.rect.y <= max_y)

    
    def show_winning_message(self, message):
        font = pygame.font.Font(None, 74)
        text_surface = font.render(message, True, (255, 255, 255))
        self.display_surface.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(20000)
        
    def show_camera_alert(self, message):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(message, True, (255, 0, 0))  # Red text for alert
        self.display_surface.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 50))  # Display near the top
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ =='__main__':
    game = Game()
    game.run()