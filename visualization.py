"""
Visualization module for Lenia using Pygame.
"""

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

        for x in range(self.lenia.size):
            for y in range(self.lenia.size):
                color = int(self.lenia.world[x, y] * 255)
                pygame.draw.rect(self.screen, (color, color, color), (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.display.flip()

    def run(self):
        """
        Run the visualization.
        """
        while True:
            self.__draw()
            self.lenia.next()
            self.clock.tick(30)

            (exit() for event in pygame.event.get() if event.type == pygame.QUIT)

if __name__ == "__main__":
    _lenia = Lenia(size=128, scale=1)
    visualizer = LeniaVisualizer(_lenia)
    visualizer.run()
