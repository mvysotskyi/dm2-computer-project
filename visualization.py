'''
Visualization module for Lenia using Pygame
'''

# Importing all of the necessary modules
import numpy as np
import pygame
from lenia import Lenia
import multiprocessing
import imageio
from PIL import Image


class LeniaVisualizer(object):
    '''
    Visualizing for LeniaVisualizer class using Pygame
    '''
    def __init__(self, lenia: Lenia, screen_width: int = 512, screen_height: int = 512):
        '''
        Initialization Visu class \

        It initializaes of all the necessary attributes
        '''
        self.lenia = lenia
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

    def __draw(self):
        pygame.display.set_caption('Lenia')
        self.screen.fill((0, 0, 0)) # Makes black screen
        # Draws the world
        cell_size = self.screen_width // self.lenia.size
        world = np.dstack(self.lenia.world) # Makes '3D-array for RGB visualization'
        world *= 255 # Scalar multiplying
        surf = pygame.surfarray.make_surface(world)
        self.screen.blit(surf, (0, 0))
        # for x in range(self.lenia.size):
        #     for y in range(self.lenia.size):
        #         # color = world[x, y] * 255
        #         pygame.draw.rect(self.screen, tuple(world[x, y]), (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.display.update()

    def run(self):
        '''
        Main loop for the visualization
        '''
        frames = []
        for _ in range(1000):

        # while True:
            self.__draw()
            self.lenia.next()
            self.clock.tick(30)

            frame = pygame.surfarray.array3d(self.screen)
            frame = Image.fromarray(frame)
            frames.append(frame)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # frame = self.screen.copy()
            # frames.append(frame)

        imageio.mimsave('lenia.gif', frames)

        # pygame.quit()
        # quit()


if __name__ == '__main__':
    _lenia = Lenia(pattern = 'pacman', size = 512, scale = 2, start_x = 5, start_y = 5)
    visualizer = LeniaVisualizer(_lenia, screen_height = 512, screen_width = 512)

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = num_processes)
    pool.map(visualizer.run(), range(num_processes))
    pool.close()
    pool.join()
