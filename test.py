from flask import json
from aiplayer import AIPlayer
from caromodel import EMPTY
from game import Game
from personplayer import PersonPlayer
from point import Point
from room import Room
from sumokugame import SumokuGame
from user import User
import jsonpickle


p1 = PersonPlayer("X", "user1")

p2 = AIPlayer("O")

players = [p1, p2]

game = SumokuGame(players, 5)
# print(json.dumps(game.__dict__))
print(jsonpickle.encode(p1, unpicklable=False))

# update board to almost getting the winner

# for pl in players:
#     print(pl.symbol)
#
#
# # give me a board that almost done, just lost some cell
# game.board = [
#     ["X", "O", "X", "O", "X"],
#     ["O", "X", "O", "X", "O"],
#     ["X", "O", "X", EMPTY, "X"],
#     ["O", "X", "O", EMPTY, "O"],
#     ["X", "O", EMPTY, EMPTY, EMPTY],
# ]
#
# # print num count of x o, in board 
# he = True
# hi = not he
# print(he, hi)
#
# x_count = 0
# o_count = 0
#     
# for i in range(game.board.__len__()):
#     for j in range(game.board[i].__len__()):
#         if game.board[j][i] == "X":
#             x_count += 1
#         elif game.board[j][i] == "O":
#             o_count += 1
#
# print(x_count, o_count)
#
# while game.getWinner() is None:
#     game.drawBoard()
#     if game.getWhoseTurn() == p1:
#         x = int(input("Enter x: "))
#         y = int(input("Enter y: "))
#         p1.move(Point(x, y))
#
#     else:
#         p2.makeMove()
#
#
# print(getattr(game.getWinner(), "symbol", None))

# i just want statis typing in each player
# for player in players:
#     print(getattr(player, 'user', None))
# how to access to property of object without error if this object don't have this property
# print(player.user)

# user1 = User("triet dep trai")
#
# room = Room("room1", user1)
# print(room.owner.name)
# print(room.owner.id)#

