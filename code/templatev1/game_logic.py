from PyQt5.QtWidgets import QLabel

from piece import Piece

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White
    x = 0
    y = 0
    boardArray = 0
    capturedWhite = 0
    capturedBlack = 0
    liberties = [[Piece().liberties] * 7 for _ in range(7)]

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

    def updateArray(self, row, col):
        if self.currentPlayer == Piece.Black:
            self.boardArray[row][col] = Piece.Black
        else:
            self.boardArray[row][col] = Piece.White

    def updateLiberties(self): # basically store each of the liberties in their respective piece places
        # keep count of the liberties surrounding on object
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if(self.boardArray[row][col] != Piece.NoPiece):
                    self.liberties[row][col] = self.checkLiberties(row, col)

    def printLibertyArray(self):
        '''prints the boardArray in an attractive way'''
        print("liberties:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.liberties]))

    def checkLiberties(self, row, col):
        count = 0
        if row > 0 and self.boardArray[row - 1][col] == 0:
            count += 1

            # Check below
        if row < 6 and self.boardArray[row + 1][col] == 0:
            count += 1

            # Check left
        if col > 0 and self.boardArray[row][col - 1] == 0:
            count += 1

            # Check right
        if col < 6 and self.boardArray[row][col + 1] == 0:
            count += 1
        return count

    def getOpponents(self, row, col, opponent):
        count = 0
        if self.getup(col, row) == None or self.getup(col, row) == opponent:
            count += 1
        if self.getright(col, row) == None or self.getright(col, row) == opponent:
            count += 1
        if self.getdown(col, row) == None or self.getdown(col, row) == opponent:
            count += 1
        if self.getleft(col, row) == None or self.getleft(col, row) == opponent:
            count += 1
        return count

    # TODO Implement capture stones/pieces | There is single capture and multiple capture
    def capture(self):  # Checking if the stones have 0 liberties
        opponent = Piece.NoPiece
        if self.currentPlayer == Piece.White:
            opponent = Piece.Black
        else:
            opponent = Piece.White
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if self.checkLiberties(row,col) == 0 and self.boardArray[row][col] != Piece.NoPiece and self.getOpponents(row,col,opponent):
                    if self.boardArray[row][col] == Piece.Black:
                        self.capturedWhite += 1

                    elif self.boardArray[row][col] == Piece.White:
                        self.capturedBlack += 1
                        self.clearSpot(row, col)
                    print(f"{self.boardArray[row][col]} Stone Captured at x: {row}, y: {col}")

    def captureMultiple(self):
        pass

    def capture_piece(self, row, col):
        # Capture a piece at the given position
        captured_piece = self.boardArray[row][col]
        if captured_piece == Piece.White:  # if the captured piece is white, add to black player score
            self.capturedBlack += 1
            return f"White Stone Captured at x: {row}, y: {col}"
        elif captured_piece == Piece.Black:  # if the captured piece is black, add to white player score
            self.capturedWhite += 1
            return f"Black Stone Captured at x: {row}, y: {col}"
        self.boardArray[row][col] = Piece.NoPiece

    def clearSpot(self, row, col):
        self.boardArray[row][col] = Piece.NoPiece

    # TODO Implement the Suicide rule
    def suicideRule(self, row, col):
        #  Set the opponent player
        opponent = Piece.NoPiece
        if self.currentPlayer == Piece.White:
            opponent = Piece.Black
        else:
            opponent = Piece.White

        print("The opponents are: ", self.getOpponents(row,col, opponent))
        if self.getOpponents(row,col,opponent) == 4:  # If there are opponents all aroung
            if row > 0 and self.checkLiberties(row-1,col) == 1:  # Check above liberties
                print("Above Liberty is 1 so no suicide")
                return False

            if row < 6 and self.checkLiberties(row+1,col) == 1:  # Check below liberties
                print("Below Liberty is 1 so no suicide!")
                return False

            if col > 0 and self.checkLiberties(row,col-1) == 1:  # Check left liberties
                print("Left Liberty is 1 so no suicide!")
                return False

            if col < 6 and self.checkLiberties(row,col+1) == 1:  # Check right liberties
                print("Right Liberty is 1 so no suicide!")
                return False
            return True
        else:
            return False

    # TODO Implement the KO rule
    def ko_rule(self):
        pass

    # TODO Get score by adding the territories and prisoners
    def getScore(self):
        pass

    # TODO Win conditions
    def winner(self):
        pass

    # TODO Array checks
    def getup(self, x, y):
        if y == 0:
            return None
        else:
            return self.boardArray[y - 1][x]  # move y coordinate upwards

    def getright(self, x, y):
        if x == 6:
            return None
        else:
            return self.boardArray[y][x + 1]  # move x coordinate to the right

    def getleft(self, x, y):
        if x == 0:
            return None
        else:
            return self.boardArray[y][x - 1]  # move x coordinate to the left

    def getdown(self, x, y):
        if y == 6:
            return None
        else:
            return self.boardArray[y + 1][x]  # move y coordinate to downwards
