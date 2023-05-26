"""
Visualization module for Lenia using Pygame.
"""

import numpy as np

import pygame
from lenia import Lenia


class LeniaVisualizer:
    """
    Visualize Lenia using Pygame.
    """
    def __init__(self, lenia: Lenia, screen_width: int = 600, screen_height: int = 600):
        self.lenia = lenia
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

    def __draw(self):
        self.screen.fill((0, 0, 0))
        # Draw the world
        cell_size = self.screen_width // self.lenia.size
        world = np.dstack(self.lenia.world)

        world *= 255
        surf = pygame.surfarray.make_surface(world)
        self.screen.blit(surf, (0, 0))
        # for x in range(self.lenia.size):
        #     for y in range(self.lenia.size):
        #         # color = world[x, y] * 255
        #         pygame.draw.rect(self.screen, tuple(world[x, y]), (x * cell_size, y * cell_size, cell_size, cell_size))

        pygame.display.update()

    def run(self):
        """
        Run the visualization.
        """
        while True:
            self.__draw()
            self.lenia.next()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    _lenia = Lenia(pattern="emitter", size=800, scale=8, start_x=5, start_y=5)
    visualizer = LeniaVisualizer(_lenia)
    visualizer.run()
