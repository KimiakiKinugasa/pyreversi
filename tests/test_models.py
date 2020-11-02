import numpy as np
from reversi.models import Board, Color, Direction, Disk, LegalActions, Position


def test_color():
    assert Color.LIGHT == Color.DARK.reverse()


def test_disk():
    assert Disk.DARK == Color.DARK
    assert Disk.LIGHT == Disk.DARK.reverse()
    assert Disk.NULL == 0
    assert str(Disk.DARK) == "x"
    assert str(Disk.LIGHT) == "o"
    assert str(Disk.NULL) == "-"


def test_position():
    assert Position(0, 0) == Position(0, 0)
    assert not Position(0, 0) == Position(0, 1)
    assert Position(0, 1) <= Position(0, 1)
    assert Position(0, 1) <= Position(0, 2)
    assert not Position(1, 1) <= Position(0, 2)
    assert Position(0, 1) + Direction(0, 1) == Position(0, 2)


def test_board():
    config = np.array(
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
        "--------\n"
    )
    board = Board(config)
    assert board.length == 8
    assert str(board) == config_str
    assert board[Position(0, 0)] == Disk.NULL


def test_legal_actions():
    legal_actions = LegalActions(np.zeros((4, 4), np.bool))
    assert not legal_actions.exists_legal_actions()
    assert not legal_actions[Position(0, 0)]
