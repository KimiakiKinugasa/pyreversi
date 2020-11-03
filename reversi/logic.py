"""reversi logic

fundamental elements and logics of reversi
"""
from __future__ import annotations

from typing import Optional, Tuple

import numpy as np

from .models import _DIRECTIONS, Board, Color, Direction, Disk, LegalActions, Position


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
            if is_legal_action(board, color, Position(row, col)):
                flags[row][col] = True
    return LegalActions(flags)


def is_legal_action(board: Board, color: Color, position: Position) -> bool:
    """legal actionか

    Args:
        board (Board): 盤の状態
        color (Color): 置きたい色
        position (Position): 置きたい位置

    Returns:
        bool: True if legal, False if illegal
    """
    if board[position] != Disk.NULL:
        return False
    # 周囲8マスに-colorがなければfalse
    # 周囲8マスに-colorがある場合，その方向に進んで，NULLにならずにcolorがあればTrue
    for direction in _DIRECTIONS:
        adjacent_position = position + direction
        # 隣の位置がマスをはみ出すか隣の位置のマスの色が-colorでないないなら
        if (
            not (
                Position(0, 0)
                <= adjacent_position
                < Position(board.length, board.length)
            )
            or board[adjacent_position] != color.reverse()
        ):
            continue
        legal, _ = _increment_search(board, color, adjacent_position, direction)
        if legal:
            return True
    return False


def _increment_search(
    board: Board, color: Color, position: Position, direction: Direction
) -> Tuple[bool, Optional[Position]]:
    """colorの位置を探す

    positionからdirectionの方向に進み，空マスに出会わず，colorのマスに到達できるか．
    到達できたら，その位置も返す

    Args:
        board (Board): 盤の状態
        color (Color): 探す色
        position (Position): 調べるマス
        direction (Direction): 探す方向

    Returns:
        Tuple[bool, Optional[Position]]: colorのマスに到達できたかの真偽値と到達した位置
    """
    if not Position(0, 0) <= position < Position(board.length, board.length):
        return False, None
    if board[position] == Disk.NULL:
        return False, None
    if board[position] == color:
        return True, position
    return _increment_search(
        board,
        color,
        position + direction,
        direction,
    )


def execute_action(board: Board, color: Color, position: Position) -> Board:
    """execute action and return new state board

    positionは必ずlegalなものを使うこと．この関数ではlegalかのチェックはしない

    Args:
        board (Board): 盤
        color (Color): 石の色
        position (Position): 石を置く場所
    Returns:
        Board: 石が置かれた新しい状態の盤
    """
    flip_position_list = [position]
    for direction in _DIRECTIONS:
        adjacent_position = position + direction
        # 隣の位置がマスをはみ出すか隣の位置のマスの色が-colorでないないなら
        if (
            not (
                Position(0, 0)
                <= adjacent_position
                < Position(board.length, board.length)
            )
            or board[adjacent_position] != color.reverse()
        ):
            continue
        legal, end_position = _increment_search(
            board, color, adjacent_position, direction
        )
        while legal and adjacent_position != end_position:
            flip_position_list.append(adjacent_position)
            adjacent_position = adjacent_position + direction

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


def exists_legal_actions(legal_actions: LegalActions) -> bool:
    """exists legal actions

    Returns:
        bool: True if exists legal actions, False if not
    """
    return np.count_nonzero(legal_actions.flags) != 0
