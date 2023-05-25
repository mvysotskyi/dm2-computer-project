"""
Game of Life 3D module.
"""

from board3d import Board3D, Sell

class GameOfLife3D:
    """
    Game of Life 3D class.
    """
    def __init__(self, board: Board3D):
        self.board = board

    def init_custom(self, custom: list[tuple[int, int, int]], translate: tuple[int, int, int] = (0, 0, 0)):
        """
        Initialize custom board.
        """
        for x, y, z in custom:
            x = x + translate[0]
            y = y + translate[1]
            z = z + translate[2]

            self.board.set(x, y, z, Sell(state=Sell.State.ALIVE))

    def init_stairs(self, x: int, y: int, z: int):
        """
        Initialize 3d glider.
        """
        translate_vec = (self.board.size // 2,) * 3
        self.init_custom([
            (x, y, z),
            (x + 1, y, z),
            (x, y + 1, z),
            (x + 1, y + 1, z),
            (x, y, z + 1),
            (x + 1, y + 1, z),
            # (x + 1, y, z+1),
            # (x, y, z + 1),
            # (x + 1, y + 1, z + 1),
        ], translate_vec)

    def __next_generation(self):
        """
        Next generation.
        """
        next_board = Board3D(size=self.board.size)
        for x in range(self.board.size):
            for y in range(self.board.size):
                for z in range(self.board.size):
                    neighbors = self.board.get_neighbours(x, y, z)
                    alive_neighbors = neighbors.count(Sell(state=Sell.State.ALIVE))

                    if self.board.get(x, y, z).is_alive():
                        if alive_neighbors in (4, 5):
                            next_board.set(x, y, z, Sell(state=Sell.State.ALIVE))
                    else:
                        if alive_neighbors == 5:
                            next_board.set(x, y, z, Sell(state=Sell.State.ALIVE))

        self.board = next_board

    def next_generation(self, n_next: int = 1):
        """
        Compute the next n generations.
        """
        for _ in range(n_next):
            self.__next_generation()

    def end_of_life(self):
        """
        Check if the board is empty.
        """
        return self.board == Board3D(size=self.board.size)
