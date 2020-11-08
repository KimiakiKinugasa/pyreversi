import numpy as np
import pytest
from numpy import array
from reversi.models import Board, Direction, Disk, Position, Square


def test_disk():
    assert Disk.LIGHT == Disk.DARK.reverse()


def test_square():
    assert Square.DARK == Disk.DARK
    assert Square.LIGHT == Disk.LIGHT
    assert Square.NULL == 0
    assert str(Square.DARK) == "x"
    assert str(Square.LIGHT) == "o"
    assert str(Square.NULL) == "-"


def test_position():
    assert Position(0, 0) == Position(0, 0)
    assert Position(0, 0) != Position(0, 1)
    assert Position(0, 1) <= Position(0, 1)
    assert Position(0, 1) <= Position(0, 2)
    assert not Position(1, 1).__le__(Position(0, 2))
    assert not Position(1, 1).__gt__(Position(0, 2))
    assert Position(0, 1) + Direction(0, 1) == Position(0, 2)
    with pytest.raises(TypeError):
        Position(0, 0) + Position(0, 1)


def test_board():
    config = array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    config_str = (
        "--------\n"
        "--------\n"
        "--------\n"
        "---xo---\n"
        "---ox---\n"
        "--------\n"
        "--------\n"
        "--------"
    )
    board = Board(config)
    assert Board(np.zeros((4, 4), dtype=np.int8)) == Board(
        np.zeros((4, 4), dtype=np.int8)
    )
    assert Board(np.zeros((4, 4), dtype=np.int8)) != Board(
        np.ones((4, 4), dtype=np.int8)
    )
    assert str(board) == config_str
    assert board == eval(repr(board))
    assert board[Position(0, 0)] == Square.NULL
    # config cannot be replaced.
    with pytest.raises(AttributeError):
        board.config = config
    with pytest.raises(ValueError):
        board.config[0][0] = Square.DARK
    # board cannot be updated
    with pytest.raises(TypeError):
        board[Position(0, 0)] = Square.DARK
    with pytest.raises(IndexError):
        board[Position(-1, -1)]
