from src.game.CasualGame import CasualGame
from src.player.PersonPlayer import PersonPlayer
from src.player.AIPlayer import AIPlayer
from src.User import User
from src.util.point import Point
from src.util.cell import Cell

game = CasualGame()

user = User("khoa")
player = PersonPlayer(user)

bot = AIPlayer()

game.addPlayer(player)
game.addPlayer(bot)

game.randomSeed()

print(game.players[0].symbol, game.players[1].symbol)

# exit(0)
while game.getWinner() is None:
    game.drawBoard()
    if game.getCurrentTurn() == player:
        x = int(input("Enter x: "))
        y = int(input("Enter y: "))
        player.move(Point(x, y))
    else:
        bot.makeMove()
