from piece import Piece

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    x = 0
    y = 0
    boardArray = 0

    def update(self, boardArray, x, y):
        self.boardArray = boardArray
        self.x = x
        self.y = y

    def checkEmpty(self, x, y): #checks if the array is '0'
        if(self.boardArray[x][y] == Piece.NoPiece):
            return True
        else:
            return False
