import os
import pygame
import random
import math



class Game:
    def __init__(self):
        # Initialize Game Window
        pygame.init()
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        pygame.display.set_caption("Dark Pursuit")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.clock = pygame.time.Clock()
        self.frame_update = 60
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill((0, 0, 0))
            scaled_display = pygame.transform.scale(self.display, self.screen.get_size())
            self.screen.blit(scaled_display, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.frame_update)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
