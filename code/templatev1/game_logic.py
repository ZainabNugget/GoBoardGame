from piece import Piece

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    currentPlayer = Piece.White
    x = 0
    y = 0
    boardArray = 0

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

