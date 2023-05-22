"""
Visualization module for Game of Life simulation.
"""

import pygame
from gameoflife import GameOfLife

class Simulation:
    """
    Simulation class.
    """

    def __init__(self, game_instance: GameOfLife, screen_size: tuple[int, int] = (800, 600)):
        self._game = game_instance
        self.screen_width, self.screen_height = screen_size

    def __draw_board(self):
        """
        Draw the board.
        """
        cell_width = self.screen_width // self._game.board.xsize
        cell_height = self.screen_height // self._game.board.ysize

        for ypos in range(self._game.board.ysize):
            for xpos in range(self._game.board.xsize):
                if self._game.board.get(xpos, ypos).is_alive():
                    pygame.draw.rect(
                        pygame.display.get_surface(),
                        (255, 255, 255),
                        (xpos * cell_width, ypos * cell_height, cell_width, cell_height)
                    )

    def __update_game(self):
        """
        Update the game.
        """
        self._game.next_generation()
        self.__draw_board()

    def run(self):
        """
        Run the simulation.
        """
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            self.__update_game()
            self.__draw_board()

            pygame.time.delay(100)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = GameOfLife(80, 60)
    game.init_gilder_gun(bias=(30, 25))
    simulation = Simulation(game)
    simulation.run()
