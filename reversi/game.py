from __future__ import annotations

from typing import Optional

from . import logic
from .models import Board, Color, LegalActions, Position


class Game:
    def __init__(self, board: Board, color: Color):
        self.current_color = color
        self.board = board
        self._legal_actions = logic.obtain_legal_actions(board, self.current_color)
        opponent_legal_actions = logic.obtain_legal_actions(
            board, Color(-self.current_color)
        )
        self._game_over = not (
            logic.exists_legal_actions(self._legal_actions)
            and logic.exists_legal_actions(opponent_legal_actions)
        )

    @staticmethod
    def init_game(length: int) -> Game:
        board = logic.init_board(length)
        return Game(board, Color.DARK)

    def is_game_over(self) -> bool:
        return self._game_over

    def get_legal_actions(self) -> LegalActions:
        return self._legal_actions

    def execute_action(self, action: Optional[Position]):
        """execute action

        Args:
            action (Optional[Position]): 石を置く場所，Noneならパス

        Raises:
            IllegalActionError: 石を置けるのにパスした場合
            IllegalActionError: 石を置けない場所を指定した場合
        """
        if not self.is_legal_action(action):
            raise IllegalActionError("不正な操作です．")
        # Noneならパスなので，boardは変わらない
        if isinstance(action, Position):
            self.board = logic.execute_action(self.board, self.current_color, action)
        self.current_color = self.current_color.reverse()
        self._legal_actions = logic.obtain_legal_actions(self.board, self.current_color)
        # 自分も相手も石を置ける場所がないなら，ゲーム終了
        self._game_over = not logic.exists_legal_actions(
            self._legal_actions
        ) and not logic.exists_legal_actions(
            logic.obtain_legal_actions(self.board, self.current_color.reverse())
        )

    def is_legal_action(self, action: Optional[Position]) -> bool:
        """is legal action

        パスできるのはlegal_actionsがない場合のみ，石を置く場合は，legalな場所のみTrue

        Args:
            action (Optional[Position]): 石を置く場所，Noneならパス

        Returns:
            bool: True if legal action, False if illegal action
        """
        return (
            action is None and not logic.exists_legal_actions(self._legal_actions)
        ) or (
            isinstance(action, Position)
            and Position(0, 0)
            <= action
            < Position(self.board.length, self.board.length)
            and self._legal_actions[action]
        )

    def count_color(self, color: logic.Color) -> int:
        return logic.count_color(self.board, color)


class IllegalActionError(ValueError):
    pass
