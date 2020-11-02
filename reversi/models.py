from __future__ import annotations

from enum import IntEnum
from typing import Final, NamedTuple

import numpy as np


class Reversible(IntEnum):
    def reverse(self):
        return self.__class__(-self)


class Color(Reversible):
    """reversi color"""

    DARK = 1
    LIGHT = -1


class Disk(Reversible):
    """State of each piece of a board

    NULL means piece is empty.
    """

    DARK = Color.DARK
    LIGHT = Color.LIGHT
    NULL = 0

    def __str__(self):
        if self.name == "DARK":
            return "x"
        if self.name == "LIGHT":
            return "o"
        if self.name == "NULL":
            return "-"


class Direction(NamedTuple):
    row: int
    col: int


_DIRECTIONS: Final = [
    Direction(-1, -1),
    Direction(-1, 0),
    Direction(-1, 1),
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, -1),
    Direction(1, 0),
    Direction(1, 1),
]


class Position(NamedTuple):
    row: int
    col: int

    def __lt__(self, position):
        if not isinstance(position, Position):
            raise TypeError("{} is not 'Position'".format(position))
        return self.row < position.row and self.col < position.col

    def __le__(self, position):
        if not isinstance(position, Position):
            raise TypeError("{} is not 'Position'".format(position))
        return self.row <= position.row and self.col <= position.col

    def __gt__(self, position):
        if not isinstance(position, Position):
            raise TypeError("{} is not 'Position'".format(position))
        return self.row > position.row and self.col > position.col

    def __ge__(self, position):
        if not isinstance(position, Position):
            raise TypeError("{} is not 'Position'".format(position))
        return self.row >= position.row and self.col >= position.col

    def __add__(self, direction):
        if not isinstance(direction, Direction):
            raise TypeError("{} is not 'Direction'".format(direction))
        return Position(self.row + direction.row, self.col + direction.col)


class LegalActions:
    """可能な操作の一覧"""

    def __init__(self, flags: np.ndarray):
        """constractor

        flagsはboardと同じ形の行列で，成分はbool

        Args:
            flags (np.ndarray): 置ける所はTrue，置けない所はFalse
            color Color: 石の色
        """
        self.flags = flags

    def __eq__(self, legal_actions):
        if not isinstance(legal_actions, LegalActions):
            return False
        return np.array_equal(self.flags, legal_actions.flags)

    def __getitem__(self, position: Position) -> bool:
        return self.flags[position]

    def __str__(self):
        return str(self.flags)

    def exists_legal_actions(self) -> bool:
        """exists legal actions

        Returns:
            bool: True if exists legal actions, False if not
        """
        return np.count_nonzero(self.flags) != 0


class Board:
    """reversi board

    This is supposed to be immutable
    """

    def __init__(self, config: np.ndarray):
        """constractor

        config must be a squire matrix. elements of config must be -1, 0, or 1.
        上記の条件はチェックしないから，外部からあんまり呼ばないで.

        Args:
            config (np.ndarray): configuration of the board
        """
        self.config = config
        self.length = len(config)

    def __eq__(self, board):
        if not isinstance(board, Board):
            return False
        return np.array_equal(self.config, board.config)

    def __getitem__(self, position: Position) -> Disk:
        return self.config[position]

    def __str__(self):
        board_str = ""
        for row in range(self.length):
            for col in range(self.length):
                board_str += str(Disk(self.config[row][col]))
            board_str += "\n"
        return board_str

    def __repr__(self):
        return "Board(\n{})".format(repr(self.config))
