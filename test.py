from src.game.TicTacToe import TicTacToe
from src.room.Room import Room
from src.User import User


# game = CasualGame()
room = Room("room", User("khoa"))
room.addCompetitor(User("bot", id="bot"))


game = TicTacToe()

room.addGame(game)

# game.addPlayer(player)
# game.addPlayer(bot)

print(room)
game.randomSeed()

# print(game.players[0].symbol, game.players[1].symbol)

# exit(0)
# while game.getWinner() is None:
#     game.drawBoard()
#     print("\n")
#     if game.getCurrentTurn() == player:
#         x, y = map(int, input("X, Y: ").split())
#         player.move(Point(x, y))
#     else:
#         bot.makeMoveSumoku()
#
# game.drawBoard()
#
# if game.getWinner().user:
#     print(game.getWinner().user.name + " wins")
# else:
#     print("Bot wins")

# x, y = map(int, input("X, Y: ").split())
# player.move(Point(x, y))
# game.drawBoard()
# print("\n")
# bot.makeMoveTictactoe()
# game.drawBoard()
# x, y = map(int, input("X, Y: ").split())
# player.move(Point(x, y))
# game.drawBoard()
# print("\n")
# bot.makeMoveTictactoe()
# game.drawBoard()
#
#
