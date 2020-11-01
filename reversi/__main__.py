import reversi.game
from reversi.logic import Color
from reversi.player import HumanPlayer

game = reversi.game.Game.init_game(4)
print(str(Color.DARK), game.count_color(Color.DARK))
print(str(Color.LIGHT), game.count_color(Color.LIGHT))

print(game.board)
while not game.is_game_over():
    action = HumanPlayer().play(game)
    if not game.is_legal_action(action):
        print("無効な操作です．")
        continue
    game.execute_action(action)
    print(game.board)
print(Color.DARK, game.count_color(Color.DARK))
print(Color.LIGHT, game.count_color(Color.LIGHT))
