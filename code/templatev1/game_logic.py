from PyQt5.QtWidgets import QLabel

from piece import Piece

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White
    x = 0
    y = 0
    boardArray = 0
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

    def update(self, boardArray, x, y):
        self.boardArray = boardArray
        self.x = x
        self.y = y

    def checkEmpty(self, x, y): #checks if the array is '0'
        if(x >= len(self.boardArray) | y >= len(self.boardArray)):
            print(x, " ", y)
            return False
        elif(self.boardArray[x][y] == Piece.NoPiece):
            return True
        else:
            return False

    def updateTurn(self):
        if(self.currentPlayer == Piece.White):
            self.currentPlayer = Piece.Black
            print("Black's turn")
        else:
            self.currentPlayer = Piece.White
            print("White's turn")
