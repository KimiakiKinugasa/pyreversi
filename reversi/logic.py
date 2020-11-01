"""reversi logic

fundamental elements and logics of reversi
"""
from __future__ import annotations

from enum import IntEnum
from typing import Optional, Tuple

import numpy as np

_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Color(IntEnum):
    """reversi color"""

    DARK = 1
    LIGHT = -1


class Disk(IntEnum):
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

    def __getitem__(self, index):
        return self.flags[index]

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

    def __getitem__(self, index):
        return self.config[index]

    def __str__(self):
        board_str = ""
        for row in range(self.length):
            for col in range(self.length):
                board_str += str(Disk(self[row][col]))
            board_str += "\n"
        return board_str

    def __repr__(self):
        return "Board(\n{})".format(repr(self.config))


def init_board(length: int):
    """initialize board

    Args:
        length (int): length of board
    """
    config = np.zeros((length, length), dtype=np.int8)
    config[length // 2][length // 2] = Disk.DARK
    config[length // 2 - 1][length // 2 - 1] = Disk.DARK
    config[length // 2][length // 2 - 1] = Disk.LIGHT
    config[length // 2 - 1][length // 2] = Disk.LIGHT
    return Board(config)


def obtain_legal_actions(board: Board, color: Color) -> LegalActions:
    """obtain legal actions

    Args:
        board (Board): 盤の状態
        color (Color): 置きたい石の色

    Returns:
        LegalActions: legal actions
    """
    flags = np.zeros((board.length, board.length), dtype=np.bool)
    for row in range(board.length):
        for col in range(board.length):
            if is_legal_action(board, color, (row, col)):
                flags[row][col] = True
    return LegalActions(flags)


def is_legal_action(board: Board, color: Color, position: Tuple[int, int]) -> bool:
    """legal actionか

    Args:
        board (Board): 盤の状態
        color (Color): 置きたい色
        position (Tuple[int, int]): 置きたい位置

    Returns:
        bool: [description]
    """
    if board[position] != Disk.NULL:
        return False
    # 周囲8マスに-colorがなければfalse
    # 周囲8マスに-colorがある場合，その方向に進んで，NULLにならずにcolorがあればTrue
    for direction in filter(
        lambda direction: 0 <= direction[0] + position[0] < board.length
        and 0 <= direction[1] + position[1] < board.length,
        _DIRECTIONS,
    ):
        adjacent_position = (position[0] + direction[0], position[1] + direction[1])
        if board[adjacent_position] != -color:
            continue
        legal, _ = _increment_search(board, color, adjacent_position, direction)
        if legal:
            return True
    return False


def _increment_search(
    board: Board, color: Color, position: Tuple[int, int], direction: Tuple[int, int]
) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """colorの位置を探す

    positionからdirectionの方向に進み，空マスに出会わず，colorのマスに到達できるか．
    到達できたら，その位置も返す

    Args:
        board (Board): 盤の状態
        color (Color): 探す色
        position (Tuple[int, int]): 調べるマス
        direction (Tuple[int, int]): 探す方向

    Returns:
        Tuple[bool, Optional[Tuple[int, int]]]: colorのマスに到達できたかの真偽値と到達した位置
    """
    if not (0 <= position[0] < board.length and 0 <= position[1] < board.length):
        return False, None
    if board[position] == Disk.NULL:
        return False, None
    if board[position] == color:
        return True, position
    return _increment_search(
        board,
        color,
        (position[0] + direction[0], position[1] + direction[1]),
        direction,
    )


def execute_action(board: Board, position: Tuple[int, int], color: Color) -> Board:
    """execute action and return new state board

    positionは必ずlegalなものを使うこと．この関数ではlegalかのチェックはしない

    Args:
        board (Board): 盤
        position (Tuple[int, int]): 石を置く場所
        color (Color): 石の色
    Returns:
        Board: 石が置かれた新しい状態の盤
    """
    flip_position_list = [position]
    for direction in filter(
        lambda direction: 0 <= direction[0] + position[0] < board.length
        and 0 <= direction[1] + position[1] < board.length,
        _DIRECTIONS,
    ):
        adjacent_position = (position[0] + direction[0], position[1] + direction[1])
        if board[adjacent_position] != -color:
            continue
        legal, end_position = _increment_search(
            board, color, adjacent_position, direction
        )
        while legal and adjacent_position != end_position:
            flip_position_list.append(adjacent_position)
            adjacent_position = (
                adjacent_position[0] + direction[0],
                adjacent_position[1] + direction[1],
            )

    # flip_position_listが1なら一枚もひっくり返らないのでlegal actionではない
    # 関数呼び出し側がちゃんとlegal actionとなるように注意する
    assert len(flip_position_list) > 1
    config = board.config.copy()
    for position in flip_position_list:
        config[position] = color
    return Board(config)


def count_color(board: Board, color: Color) -> int:
    """count color

    Args:
        board (Board): 盤の状態
        color (Color): 数えたい色

    Returns:
        int: 数えたい色の数
    """
    return np.sum(board.config == color)
