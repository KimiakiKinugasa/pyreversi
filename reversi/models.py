from __future__ import annotations

from enum import IntEnum
from typing import Final, NamedTuple

import numpy as np


class Reversible(IntEnum):
    def reverse(self):
        return self.__class__(-self)


class Disk(Reversible):
    """reversi disk"""

    DARK = 1
    LIGHT = -1


class Square(Reversible):
    """State of each piece of a board

    NULL means piece is empty.
    """

    DARK = Disk.DARK
    LIGHT = Disk.LIGHT
    NULL = 0

    def __str__(self):
        if self == self.DARK:
            return "x"
        if self == self.LIGHT:
            return "o"
        return "-"


class Direction(NamedTuple):
    row: int
    col: int


_DIRECTIONS: Final = (
    Direction(-1, -1),
    Direction(-1, 0),
    Direction(-1, 1),
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, -1),
    Direction(1, 0),
    Direction(1, 1),
)


class Position(NamedTuple):
    row: int
    col: int

    def __lt__(self, position):
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row < position.row and self.col < position.col

    def __le__(self, position):
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row <= position.row and self.col <= position.col

    def __gt__(self, position):
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row > position.row and self.col > position.col

    def __ge__(self, position):
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row >= position.row and self.col >= position.col

    def __add__(self, direction):
        if not isinstance(direction, Direction):
            raise TypeError(f"{direction} is not 'Direction'")
        return Position(self.row + direction.row, self.col + direction.col)


class Board:
    """reversi board

    This is supposed to be immutable
    """

    def __init__(self, config: np.ndarray):
        """constractor

        config must be a squire matrix. elements of config must be -1, 0, or 1.
        上記の条件はチェックしないから，外部から呼ぶ場合は注意すること．

        Args:
            config (np.ndarray): configuration of the board
        """
        self._config = config.copy()
        self._config.setflags(write=False)

    def __eq__(self, board):
        return isinstance(board, Board) and np.array_equal(self._config, board._config)

    def __ne__(self, board):
        return not self.__eq__(board)

    def __getitem__(self, position) -> Square:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        if not self.is_in_range(position):
            raise IndexError(f"{position} is out of range")
        return self._config[position]

    def __str__(self):
        board_str = ""
        for row in range(len(self._config)):
            for col in range(len(self._config)):
                board_str += str(Square(self[Position(row, col)]))
            board_str += "\n"
        return board_str

    def __repr__(self):
        return f"Board(\n{repr(self._config)})"

    @property
    def config(self):
        return self._config

    def is_in_range(self, position: Position) -> bool:
        return Position(0, 0) <= position < Position(*self._config.shape)
