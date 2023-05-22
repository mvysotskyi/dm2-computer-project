"""
Game of Life module.
"""

from board import Board, Sell


class GameOfLife:
    """
    Game of Life class.
    """
    def __init__(self, xsize: int = 1, ysize: int = 1):
        self.board = Board(xsize, ysize)

    def init_custom(self, alive_sells: list[tuple[int, int]], bias: tuple[int, int] = (0, 0)):
        """
        Initialize the board with the given alive sells.
        """
        for sell in alive_sells:
            if not self.board.valid_position(sell[0], sell[1]):
                raise ValueError("Invalid position.")

            self.board.set(sell[0] + bias[0], sell[1] + bias[1], Sell(Sell.State.ALIVE))

        self.__next_generation()

    def init_rpentomino(self, bias: tuple[int, int] = (0, 0)):
        """
        Initialize the board with the R-pentomino.
        """
        self.init_custom([(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)], bias)

    def init_diehard(self, bias: tuple[int, int] = (0, 0)):
        """
        Initialize the board with the diehard.
        """
        self.init_custom([(6, 0), (0, 1), (1, 1), (1, 2), (5, 2), (6, 2), (7, 2)], bias)

    def init_gilder_gun(self, bias: tuple[int, int] = (0, 0)):
        """
        Initialize the board with the gilder gun.
        """
        self.init_custom([(24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
                          (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3), (0, 4), (1, 4), (10, 4), (16, 4),
                          (20, 4), (21, 4), (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), (24, 5),
                          (10, 6), (16, 6), (24, 6), (11, 7), (15, 7), (12, 8), (13, 8)], bias)

    def __next_generation(self):
        """
        Compute the next generation.
        """
        next_board = Board(self.board.xsize, self.board.ysize)
        for ypos in range(self.board.ysize):
            for xpos in range(self.board.xsize):
                neighbours = self.board.get_neighbours(xpos, ypos)
                alive_neighbours = neighbours.count(Sell(Sell.State.ALIVE))

                if self.board.get(xpos, ypos).is_alive():
                    if alive_neighbours in (2, 3):
                        next_board.set(xpos, ypos, Sell(Sell.State.ALIVE))
                else:
                    if alive_neighbours == 3:
                        next_board.set(xpos, ypos, Sell(Sell.State.ALIVE))

        self.board = next_board

    def next_generation(self, n_next: int = 1):
        """
        Compute the next n generations.
        """
        for _ in range(n_next):
            self.__next_generation()

    def end_of_life(self):
        """
        Check if the game is over.
        """
        return self.board == Board(self.board.xsize, self.board.ysize)
