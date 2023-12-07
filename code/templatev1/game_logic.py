from PyQt5.QtWidgets import QLabel

from piece import Piece


class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White

    def currentPlayer(self):
        self.current_turn_label = QLabel("Current Turn: -")
        self.player_scores_label = QLabel("Scores: Player 1: -  Player 2: -")

        # current player
        self.current_player = QLabel()
        self.current_player.setNum(self.currentPlayer)

        # player score & turn
        self.isPlayer1Turn = True
        self.player1Score = 0
        self.playerUnoScore = QLabel()
        self.playerUnoScore.setNum(self.player1Score)
        self.player2Score = 0
        self.playerDosScore = QLabel()
        self.playerDosScore.setNum(self.player2Score)
