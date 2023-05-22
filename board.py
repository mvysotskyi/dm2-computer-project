"""
Board module for game of life simulation.
"""

from enum import Enum
from copy import deepcopy

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


class Board:
    """
    Board class for game of life simulation.
    """
    def __init__(self, xsize: int = 1, ysize: int = 1, default: Sell = Sell(Sell.State.DEAD)):
        self.xsize = xsize
        self.ysize = ysize
        self.board = [[default for _ in range(xsize)] for __ in range(ysize)]

    def __str__(self):
        result = ""
        boundary = " - " * (self.xsize + 2) + "\n"

        for row in self.board:
            row = list(map(lambda cell: f" {chr(0x2588) * 2}" if cell.is_alive() else "   ", row))
            result += "".join(row) + "\n"

        return boundary + result + boundary

    def __repr__(self):
        return f"{__class__.__name__}(xsize={self.xsize}, ysize={self.ysize})"

    def __eq__(self, other: "Board") -> bool:
        return self.board == other.board

    def valid_position(self, xpos: int, ypos: int) -> bool:
        """
        Check if the given position is valid.
        """
        return 0 <= xpos < self.xsize and 0 <= ypos < self.ysize

    def copy(self):
        """
        Return a copy of the board.
        """
        return deepcopy(self)

    def get(self, xpos: int, ypos: int) -> Sell:
        """
        Get the value of the cell at the given position.
        """
        return self.board[ypos][xpos]

    def set(self, xpos: int, ypos: int, cell: Sell):
        """
        Set the value of the cell at the given position.
        """
        self.board[ypos][xpos] = cell

    def get_neighbours(self, xpos: int, ypos: int) -> list[Sell]:
        """
        Get the values of the neighbours of the cell at the given position.
        """
        neighbours = []
        for ycoord in range(ypos - 1, ypos + 2):
            for xcoord in range(xpos - 1, xpos + 2):
                if (xcoord, ycoord) != (xpos, ypos) and self.valid_position(xcoord, ycoord):
                    neighbours.append(self.get(xcoord, ycoord))

        return neighbours
