"""
3d world board for Game of Life.
"""

from enum import Enum

import numpy as np

class Sell:
    """
    Sell class.
    """
    class State(Enum):
        """
        Sell state enumeration.
        """
        DEAD = 0
        ALIVE = 1

    def __init__(self, state: State = State.DEAD):
        self.state = state

    def __str__(self):
        return f"{__class__.__name__}: {self.state}"

    def __repr__(self):
        return f"{__class__.__name__}(state={self.state})"

    def __eq__(self, other: "Sell") -> bool:
        return self.state == other.state

    def is_alive(self) -> bool:
        """
        Check if the sell is alive.
        """
        return self.state == self.State.ALIVE

    def make_alive(self):
        """
        Make the sell alive.
        """
        self.state = self.State.ALIVE

    def make_dead(self):
        """
        Make the sell dead.
        """
        self.state = self.State.DEAD

class Board3D:
    """
    3d world board.
    """
    def __init__(self, size: int = 10):
        self.size = size
        self.board = np.array(
            [[[Sell() for _ in range(size)] for _ in range(size)] for _ in range(size)]
        )

    def __str__(self):
        return f"{__class__.__name__}: {self.board}"

    def __repr__(self):
        return f"{__class__.__name__}(size={self.size})"

    def __eq__(self, other: "Board3D") -> bool:
        return self.board == other.board

    def valid_position(self, xpos: int, ypos: int, zpos: int) -> bool:
        """
        Check if the given position is valid.
        """
        return 0 <= xpos < self.size and 0 <= ypos < self.size and 0 <= zpos < self.size

    def get(self, xpos: int, ypos: int, zpos: int) -> Sell:
        """
        Get sell by position.
        """
        return self.board[xpos][ypos][zpos]

    def set(self, xpos: int, ypos: int, zpos: int, sell: Sell):
        """
        Set sell by position.
        """
        self.board[xpos][ypos][zpos] = sell

    def get_neighbours(self, xpos: int, ypos: int, zpos: int) -> list:
        """
        Get sell neighbours.
        """
        neighbours = []
        for xcoord in range(xpos - 1, xpos + 2):
            for ycoord in range(ypos - 1, ypos + 2):
                for zcoord in range(zpos - 1, zpos + 2):
                    if (xcoord, ycoord, zcoord) != (xpos, ypos, zpos) and self.valid_position(xcoord, ycoord, zcoord):
                        neighbours.append(self.get(xcoord, ycoord, zcoord))

        return neighbours
