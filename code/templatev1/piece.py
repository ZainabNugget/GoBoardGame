class Piece(object):
    NoPiece = 0
    White = 1
    Black = 2

    def __init__(self):
        self.color = self.NoPiece  # first Piece is 0
        self.liberties = 0
