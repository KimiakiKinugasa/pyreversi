from typing import Optional, Tuple

from .game import Game
from .logic import Color


class Player:
    color: Color

    def set_color(self, color: Color):
        self.color = color

    def play(self, game):
        pass


class HumanPlayer(Player):
    def play(self, game: Game):
        legal_actions = game.get_legal_actions()
        length = game.board.length
        for row in range(length):
            for col in range(length):
                if legal_actions[row][col]:
                    print("[", row, col, end=" ] ")
        action: Optional[Tuple[int, int]]
        while True:
            input_action = input()
            if input_action == "pass":
                if not legal_actions.exists_legal_actions():
                    action = None
                    break
            input_a = input_action.split(" ")
            if len(input_a) == 2:
                try:
                    row, col = [int(i) for i in input_a]
                    if 0 <= row < length and 0 <= col < length:
                        if legal_actions[row][col]:
                            action = (row, col)
                            break
                except ValueError:
                    # Input needs to be an integer
                    print("Invalid integer")
            print("Invalid action")
        return action
