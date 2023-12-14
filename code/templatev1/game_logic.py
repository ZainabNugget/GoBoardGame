from PyQt5.QtWidgets import QLabel

from piece import Piece

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White
    x = 0
    y = 0
    boardArray = 0
    liberties = [] # This will contain the liberties of the board stuff
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

    def checkEmpty(self, row, col): #checks if the array is '0'
        if(self.boardArray[row][col] == Piece.NoPiece):
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

    def updateArray(self, row, col, object):
        self.boardArray[row][col] = object

    def updateLiberties(self): # basically store each of the liberties in their respective piece places
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if(self.boardArray[row][col] == Piece.NoPiece):
                    pass
                else:
                    # check up, down , left and right
                    print(self.getup(self.boardArray,row,col))

    # TODO Array checks
    def getup(self, boardArray, x, y):
        if y == 0:
            return None
        else:
            return boardArray[y - 1][x]  # move y coordinate upwards

    def getright(self, boardArray):
        if self.x == 6:
            return None
        else:
            return boardArray[self.y][self.x + 1]  # move x coordinate to the right

    def getleft(self, boardArray):
        if self.x == 0:
            return None
        else:
            return boardArray[self.y][self.x - 1]  # move x coordinate to the left

    def getdown(self, boardArray):
        if self.y == 6:
            return None
        else:
            return boardArray[self.y + 1][self.x]  # move y coordinate to downwards

    # TODO Implement capture stones/pieces | There is single capture and multiple capture
    def capture(self):
        pass

    # TODO Implement the Suicide rule
    def suicideRule(self):
        pass

    # TODO Implement the KO rule
    def ko_rule(self):
        pass

    # TODO Get score by adding the territories and prisoners
    def getScore(self):
        pass

    # TODO Win conditions
    def winner(self):
        pass