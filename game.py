import os, sys
import pygame

from os.path import join
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation

class Game:
    def __init__(self):
        # Initialize Game Window
        pygame.init()
        SCREEN_WIDTH = 1152
        SCREEN_HEIGHT = 624
        pygame.display.set_caption("Dark Pursuit")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.frame_update = 60
        self.running = True

        self.assets = {
            'background': load_image(join('background.png')),
            'stone': load_images(join('tiles', 'stone')),
        }

        self.tilemap = Tilemap(self, tile_size=16)
        tilemap_path = 'data/entities/maps/0.json'
        if not os.path.exists(tilemap_path):
            raise FileNotFoundError(f"Tilemap file not found: {tilemap_path}")
        self.tilemap.load(tilemap_path)
        print(f"Tilemap loaded from {tilemap_path}")

    def run(self):
        while self.running:
            self.display.fill((0, 0, 0, 0))
            self.display.blit(self.assets['background'], (0, 0))
            render_scroll = (0, 0)
            self.tilemap.render(self.display, offset=render_scroll)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.frame_update)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
