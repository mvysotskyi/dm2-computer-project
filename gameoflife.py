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
