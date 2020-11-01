import numpy as np
from reversi.logic import Board, Disk, init_board


def test_disk():
    assert Disk.DARK == 1
    assert Disk.LIGHT == -Disk.DARK
    assert Disk.NULL == 0
    assert str(Disk.DARK) == "x"
    assert str(Disk.LIGHT) == "o"
    assert str(Disk.NULL) == "-"


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
    board = init_board(8)
    # print(board)
    assert Board(config).length == 8
    assert board == Board(config)
    assert str(board) == config_str
