from piece import Piece


class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White  # current player
    x = 0  # mouse click x position
    y = 0  # mouse click y position
    boardArray = 0  # board array

    # White scores
    capturedWhite = 0
    whiteTerritory = 0
    whiteScore = 0

    # Black scores
    capturedBlack = 0
    blackTerritory = 0
    blackScore = 0

    # TODO implement checks for spot in an array
    '''
    Takes in the row, col parameters
    checks for specific spot if empty
    returns True of False accordingly
    '''
    def checkEmpty(self, row, col):  # checks if the array is 'Piece.NoPiece' or '0'
        if self.boardArray[row][col] == Piece.NoPiece:
            return True  # it's empty
        else:
            return False  # it's not empty

    '''
    Method to update specific row, col
    '''
    def updateArray(self, row, col):
        if self.currentPlayer == Piece.Black:
            self.boardArray[row][col] = Piece.Black
        else:
            self.boardArray[row][col] = Piece.White

    # TODO update the players turn
    def updateTurn(self):  # change turn based on current player
        if self.currentPlayer == Piece.White:
            self.currentPlayer = Piece.Black
        else:
            self.currentPlayer = Piece.White

    # TODO Check the liberties of a stone on the board
    '''
    Checks the liberties of a piece by checking,
    up, down, left and right
    '''
    def checkLiberties(self, row, col):
        count = 0  # count for liberties
        if row > 0 and self.boardArray[row - 1][col] == 0:  # check up
            count += 1

        if row < 6 and self.boardArray[row + 1][col] == 0:  # check below
            count += 1

        if col > 0 and self.boardArray[row][col - 1] == 0:  # check left
            count += 1

        if col < 6 and self.boardArray[row][col + 1] == 0:  # check right
            count += 1
        return count  # return amount of liberties

    # TODO Get the white and black territories
    def updateTerritory(self):
        white = 0
        black = 0
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if self.boardArray[row][col] != Piece.NoPiece:
                    if self.boardArray[row][col] == Piece.Black:
                        black += 1
                    else:
                        white += 1
        self.whiteTerritory = white
        self.blackTerritory = black
        print("Black T: ", self.blackTerritory, " Whites: ", self.whiteTerritory)

    # TODO Get score by adding the territories and prisoners
    def updateScores(self):
        self.whiteScore = self.whiteTerritory + self.capturedWhite
        self.blackScore = self.blackTerritory + self.capturedBlack

    # TODO Implement capture stones/pieces | There is single capture and multiple capture
    '''
    For a single capture,
    - check for four opponents
    - check if not a 0 (No Piece)
    - check if liberties are 0
    '''
    def capture(self):  # Checking if the stones have 0 liberties
        opponent = Piece.NoPiece
        if self.currentPlayer == Piece.White:
            opponent = Piece.Black
        else:
            opponent = Piece.White
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if self.checkLiberties(row, col) == 0 and self.boardArray[row][col] != Piece.NoPiece and self.getOpponents(row, col, opponent) == 4:
                    if self.boardArray[row][col] == Piece.Black:
                        self.capturedWhite += 1
                        self.whiteTerritory -= 1
                        self.clearSpot(row, col)
                    elif self.boardArray[row][col] == Piece.White:
                        self.capturedBlack += 1
                        self.blackTerritory -= 1
                        self.clearSpot(row, col)
                    print(f"{self.boardArray[row][col]} Stone Captured at x: {row}, y: {col}")

    # TODO Implement capture multiple stones on board
    '''
    For a mulitple capture,
    - check if not a 0 (No Piece) or None
    - check if liberties are 0
    '''
    def captureMultiple(self):
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if self.getup(row, col) is not None and self.checkLiberties(row, col) == 0 and self.getup(row, col) != Piece.NoPiece:
                    self.capturePiece(row, col)
                elif self.getright(row, col) is not None and self.checkLiberties(row, col) == 0 and self.getright(row, col) != Piece.NoPiece:
                    self.capturePiece(row, col)
                elif self.getleft(row, col) is not None and self.checkLiberties(row, col) == 0 and self.getleft(row, col) != Piece.NoPiece:
                    self.capturePiece(row, col)
                elif self.getdown(row, col) is not None and self.checkLiberties(row, col) == 0 and self.getdown(row, col) != Piece.NoPiece:
                    self.capturePiece(row, col)

    def capturePiece(self, row, col):
        if self.boardArray[row][col] == Piece.White:
            self.capturedBlack += 1
            self.clearSpot(row, col)
            return f"White Stone Captured at x: {row}, y: {col}"
        elif self.boardArray[row][col] == Piece.Black:
            self.capturedWhite += 1
            self.clearSpot(row, col)

    # TODO Implement the Suicide rule
    '''
    Suicide rule
    - Checks for liberties around a spot
    - Checks for opponents
    - If 4 opponents, suicide!
    '''
    def suicideRule(self, row, col):
        opponent = Piece.NoPiece
        if self.currentPlayer == Piece.Black:  # set the opponent player
            opponent = Piece.White
        else:
            opponent = Piece.Black

        print("The opponents are: ", self.getOpponents(row, col, opponent))
        if self.getOpponents(row, col, opponent) == 4:  # If there are opponents all around
            if row > 0 and self.checkLiberties(row - 1, col) == 1:  # Check above liberties
                return False

            if row < 6 and self.checkLiberties(row + 1, col) == 1:  # Check below liberties
                return False

            if col > 0 and self.checkLiberties(row, col - 1) == 1:  # Check left liberties
                return False

            if col < 6 and self.checkLiberties(row, col + 1) == 1:  # Check right liberties
                return False
            return True  # return true for suicide
        else:
            return False

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

    def clearSpot(self, row, col):
        self.boardArray[row][col] = Piece.NoPiece

    '''
    Checks all sides for the opposite player
    returns a count of all opposite players!
    '''

    def getOpponents(self, row, col, opponent):
        count = 0
        if self.getup(col, row) is None or self.getup(col, row) == opponent:
            count += 1
        if self.getright(col, row) is None or self.getright(col, row) == opponent:
            count += 1
        if self.getdown(col, row) is None or self.getdown(col, row) == opponent:
            count += 1
        if self.getleft(col, row) is None or self.getleft(col, row) == opponent:
            count += 1
        return count
