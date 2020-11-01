import numpy as np
from reversi.logic import (
    Board,
    LegalActions,
    _increment_search,
    execute_action,
    init_board,
    is_legal_action,
    obtain_legal_actions,
)


def test_is_legal_action():
    board = init_board(4)
    assert not is_legal_action(board, 1, (0, 0))
    assert not is_legal_action(board, 1, (0, 1))
    assert is_legal_action(board, 1, (0, 2))


def test_increment_search():
    config = np.array(
        [
            [1, -1, -1, 0],
            [0, 1, -1, 0],
            [0, 0, 0, 0],
            [0, 1, -1, 0],
        ]
    )
    board = Board(config)
    assert _increment_search(board, 1, (3, 1), (0, -1)) == (True, (3, 1))
    assert _increment_search(board, 1, (3, 2), (0, -1)) == (True, (3, 1))
    assert _increment_search(board, 1, (3, 3), (0, -1)) == (False, None)
    assert _increment_search(board, 1, (0, 1), (0, -1)) == (True, (0, 0))
    assert _increment_search(board, 1, (0, 2), (0, -1)) == (True, (0, 0))
    assert _increment_search(board, 1, (0, 3), (0, -1)) == (False, None)


def test_obtain_legal_actions():
    board = init_board(4)
    flags = np.zeros((4, 4), dtype=np.bool)
    flags[(0, 2)] = True
    flags[(1, 3)] = True
    flags[(2, 0)] = True
    flags[(3, 1)] = True
    assert obtain_legal_actions(board, 1) == LegalActions(flags)
    board = Board(np.zeros((4, 4), dtype=np.int8))
    assert obtain_legal_actions(board, 1) == LegalActions(
        np.zeros((4, 4), dtype=np.int8)
    )


def test_execute_action():
    board = init_board(4)
    new_board = execute_action(board, (1, 3), 1)
    config = np.array(
        [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, -1, 1, 0],
            [0, 0, 0, 0],
        ]
    )
    assert new_board == Board(config)

    config = np.array(
        [
            [0, -1, -1, 1],
            [-1, -1, -1, 1],
            [1, -1, -1, 1],
            [0, -1, -1, 1],
        ],
        dtype=np.int8,
    )
    board = Board(config)
    new_board = execute_action(board, (0, 0), 1)
    after_config = np.array(
        [
            [1, 1, 1, 1],
            [1, 1, -1, 1],
            [1, -1, 1, 1],
            [0, -1, -1, 1],
        ],
        dtype=np.int8,
    )
    assert new_board == Board(after_config)


def test_exists_legal_actions():
    board = init_board(4)
    assert obtain_legal_actions(board, 1).exists_legal_actions()
    board = Board(np.zeros((4, 4), dtype=np.int8))
    assert not obtain_legal_actions(board, 1).exists_legal_actions()
