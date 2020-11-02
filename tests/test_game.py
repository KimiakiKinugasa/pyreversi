import numpy as np
import pytest
from reversi.game import Game, IllegalActionError
from reversi.logic import init_board, obtain_legal_actions
from reversi.models import Board, Color, LegalActions, Position


def test_init_game():
    game = Game.init_game(8)
    assert game.current_color == Color.DARK
    assert game.board == init_board(8)
    assert game.get_legal_actions() == obtain_legal_actions(init_board(8), Color.DARK)
    assert game.is_game_over() is False


def test_game_over():
    board = Board(np.zeros((8, 8), dtype=np.int8))
    game = Game(board, Color.LIGHT)
    assert game.is_game_over() is True


def test_execute_action():
    game = Game.init_game(4)
    game.execute_action(Position(0, 2))
    config = np.array(
        [
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, -1, 1, 0],
            [0, 0, 0, 0],
        ],
        dtype=np.int8,
    )
    flags = np.array(
        [
            [0, 1, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ],
        dtype=np.bool,
    )
    assert game.board == Board(config)
    assert game.current_color == Color.LIGHT
    assert game.get_legal_actions() == LegalActions(flags)
    assert game.is_game_over() is False

    config = np.array(
        [
            [1, -1, -1, 1],
            [0, -1, -1, 1],
            [1, -1, -1, 1],
            [1, -1, 1, 1],
        ],
        dtype=np.int8,
    )
    game = Game(Board(config), Color.LIGHT)
    assert game.get_legal_actions() == LegalActions(np.zeros((4, 4), dtype=np.bool))
    with pytest.raises(IllegalActionError):
        game.execute_action(Position(0, 0))
    with pytest.raises(IllegalActionError):
        game.execute_action(Position(1, 0))
    game.execute_action(None)
    assert game.current_color == Color.DARK
    assert game.board == Board(config)
    with pytest.raises(IllegalActionError):
        game.execute_action(None)
    game.execute_action(Position(1, 0))
    after_config = np.array(
        [
            [1, -1, -1, 1],
            [1, 1, 1, 1],
            [1, 1, -1, 1],
            [1, -1, 1, 1],
        ],
        dtype=np.int8,
    )
    assert game.board == Board(after_config)
    assert game.get_legal_actions() == LegalActions(np.zeros((4, 4), dtype=np.bool))
    assert game.is_game_over() is True
