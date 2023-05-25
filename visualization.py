"""
Visualization of Game Of Life in 3D.
"""

import pygame as pg

from object import Object3D
from camera import Camera
from projection import Projection

from board3d import Board3D
from gameoflife3d import GameOfLife3D

class Simualtion:
    """
    Software render class.
    """
    def __init__(self, game: GameOfLife3D, screen_width: int = 800, screen_height: int = 600):
        self.game = game
        self.board: Board3D = game.board

        self.screen_width, self.screen_height = screen_width, screen_height
        self.fps = 30

        pg.init()
        pg.display.set_caption('Game Of Life 3D')

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.camera = Camera([-5, 6, -55], self.screen_height / self.screen_width)
        self.projection = Projection(self)

        self.objects: list[Object3D] = []
        self.area_cube = Object3D(
            self,
            self.make_cube(0, 0, 0, self.board.size),
            self.make_cube_faces()
        )

    @staticmethod
    def make_cube(xpos, ypos, zpos, size, translate_vec: tuple[int, int, int] = (0, 0, 0)):
        """
        Make cube.
        """
        xpos += translate_vec[0]
        ypos += translate_vec[1]
        zpos += translate_vec[2]

        return [
            [xpos, ypos, zpos, 1],
            [xpos + size, ypos, zpos, 1],
            [xpos + size, ypos + size, zpos, 1],
            [xpos, ypos + size, zpos, 1],
            [xpos, ypos, zpos + size, 1],
            [xpos + size, ypos, zpos + size, 1],
            [xpos + size, ypos + size, zpos + size, 1],
            [xpos, ypos + size, zpos + size, 1]
        ]

    @staticmethod
    def make_cube_faces(bias: int = 0):
        """
        Make cube faces.
        """
        return [
            [0 + bias, 1 + bias, 2 + bias, 3 + bias],
            [0 + bias, 4 + bias, 5 + bias, 1 + bias],
            [1 + bias, 5 + bias, 6 + bias, 2 + bias],
            [2 + bias, 6 + bias, 7 + bias, 3 + bias],
            [3 + bias, 7 + bias, 4 + bias, 0 + bias],
            [4 + bias, 7 + bias, 6 + bias, 5 + bias]
        ]

    def __draw_3d_board(self):
        """
        Draw 3d board.
        """
        self.board = self.game.board
        for xpos in range(self.board.size):
            for ypos in range(self.board.size):
                for zpos in range(self.board.size):
                    if self.board.get(xpos, ypos, zpos).is_alive():
                        self.objects.append(
                            Object3D(
                                self,
                                self.make_cube(xpos, ypos, zpos, 1),
                                self.make_cube_faces()
                            )
                        )

    def __draw(self):
        self.screen.fill((0, 0, 0))
        self.area_cube.draw()

        self.__draw_3d_board()
        for obj in self.objects:
            obj.draw()

    def run(self):
        """
        Run the application.
        """
        while True:
            self.objects.clear()
            self.game.next_generation()

            self.__draw()
            self.camera.control()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            pg.display.flip()
            pg.time.delay(60)


if __name__ == '__main__':
    game = GameOfLife3D(Board3D(30))
    game.init_stairs(0, 0, 0)

    app = Simualtion(game)
    app.run()
