import random
from typing import Optional

from .game import Game
from .models import Disk, Position


class Player:
    disk: Disk

    def set_disk(self, disk: Disk):
        self.disk = disk

    def play(self, game):
        pass


class RandomPlayer(Player):
    def play(self, game: Game) -> Optional[Position]:
        legal_actions = game.get_legal_actions()
        if not legal_actions:
            return None
        return random.choice(list(legal_actions))


class HumanPlayer(Player):
    def play(self, game: Game) -> Optional[Position]:
        legal_actions = game.get_legal_actions()
        length = game.board.length
        for row in range(length):
            for col in range(length):
                if Position(row, col) in legal_actions:
                    print("[", row, col, end=" ] ")
        action: Optional[Position]
        while True:
            input_action = input()
            if input_action == "pass":
                if not legal_actions:
                    action = None
                    break
            input_a = input_action.split(" ")
            if len(input_a) == 2:
                try:
                    row, col = [int(i) for i in input_a]
                    if 0 <= row < length and 0 <= col < length:
                        if Position(row, col) in legal_actions:
                            action = Position(row, col)
                            break
                except ValueError:
                    # Input needs to be an integer
                    print("Invalid integer")
            print("Invalid action")
        return action
