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
        self._flags = flags.copy()
        self._flags.setflags(write=False)

    def __eq__(self, legal_actions):

        return isinstance(legal_actions, LegalActions) and np.array_equal(
            self._flags, legal_actions.flags
        )

    def __getitem__(self, position: Position) -> bool:
        return self._flags[position]

    def __str__(self):
        return str(self._flags)

    def __repr__(self):
        return "LegalActions(\n{})".format(repr(self._flags))

    @property
    def flags(self):
        return self._flags


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
        self._length = len(config)

    def __eq__(self, board):
        return isinstance(board, Board) and np.array_equal(self._config, board.config)

    def __getitem__(self, position: Position) -> Disk:
        return self._config[position]

    def __str__(self):
        board_str = ""
        for row in range(self._length):
            for col in range(self._length):
                board_str += str(Disk(self[Position(row, col)]))
            board_str += "\n"
        return board_str

    def __repr__(self):
        return "Board(\n{})".format(repr(self._config))

    @property
    def config(self):
        return self._config

    @property
    def length(self):
        return self._length
