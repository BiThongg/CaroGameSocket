from User import User
from model.TictactoeModel import TictactoeModel
from model.SumokuModel import CaroModel
from player.Player import Player
from util.point import Point
from util.cell import Cell
from game.CasualGame import *
from game.TicTacToe import *
from typing import Type, Callable, Dict
from model.SumoKuAI import SumokuAI


class AIPlayer(Player):
    def __init__(self, user: User | None):
        super().__init__(user)
        self.models = {
            CasualGame.__name__: SumokuAI(),
            TicTacToe.__name__: TictactoeModel(),
        }
        print(self.models, self.game)

    def makeMove(self):
        if self.game is None:
            raise ValueError("No game has been set for the AIPlayer.")

        game_name = self.game.__class__.__name__
        if game_name not in self.models:
            raise ValueError(f"No model available for game: {game_name}")

        model = self.models[game_name]
        cloneboard = self.deepCopyBoard(self.game.board)
        move = model.predict_move(cloneboard, self.symbol)

        if move:
            super().move(move)
            self.game.latestPoint = move
        else:
            raise Exception("No valid moves available.")

    def deepCopyBoard(self, board):
        return [row[:] for row in board]
