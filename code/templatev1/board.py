from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QMouseEvent
from PyQt5.QtCore import Qt
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    posX = 0
    posY = 0

    def __init__(self, parent):
        super().__init__(parent)
        #self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        # TODO - create a 2d int/Piece array to store the state of the game
        rows, cols = (self.boardWidth, self.boardHeight)
        self.boardArray = [[Piece.NoPiece] * cols for _ in range(rows)]
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        x = event.pos().x()  # x position of mouse click
        y = event.pos().y()  # y position of mouse click

        # Calculate the column and row based on the mouse coordinates
        col = int(x / self.squareWidth())
        row = int(y / self.squareHeight())

        return col, row

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / 8

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / 8

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)
        # self.placePiece(painter)

    def mousePressEvent(self, event:QMouseEvent):
        '''this event is automatically called when the mouse is pressed'''
        x = event.position().x() # x position of mouse click
        y = event.position().y() # y position of mouse click
        self.posX = event.position().x()
        self.posY = event.position().y()
        clickLoc = f"Click location: [{x}, {y}]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        self.boardArray = [[0 for self.boardHeight in range(7)] for self.boardWidth in range(7)]
        print("reset board" + self.boardArray)

        '''
        for row in range(self.boardHeight):
            for col in range(self.boardWidth):
            self.boardArray[row][col] = Piece.NoPiece
        self.printBoardArray
        '''

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # setting the default colour of the brush
        brush = QBrush(Qt.SolidPattern)  # calling SolidPattern to a variable
        brush.setColor(QColor(245, 173, 66))  # setting color to orange
        painter.setBrush(brush)  # setting brush color to painter

        for row in range(1, Board.boardHeight+1):
            for col in range(1, Board.boardWidth+1):
                    painter.save()

                    # Set the Col and Row values
                    colTransformation = self.squareWidth() * col
                    rowTransformation = self.squareHeight() * row
                    painter.translate(colTransformation, rowTransformation)

                    # Skips the extra boxes we dont need
                    if (row == Board.boardHeight or col == Board.boardWidth):
                        pass
                    else:
                        painter.fillRect(col, row, int(self.squareWidth()), int(self.squareHeight()),brush)

                    # Make small circles
                    radius = int((5 - 2) / 2)
                    center = QPoint(radius, radius)
                    painter.drawEllipse(center, radius, radius)
                    painter.restore()

                    # Changing the colour of the brush so that a slightly different colored board is drawn
                    if brush.color() == QColor(245, 173, 66):
                        brush.setColor(QColor(237, 171, 71))
                    else:
                        brush.setColor(QColor(245, 173, 66))


    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                # # TODO draw some pieces as ellipses
                # # TODO choose your color and set the painter brush to the correct color
                    painter.save()
                    colTransformation = self.squareWidth() * col
                    rowTransformation = self.squareHeight() * row
                    painter.translate(colTransformation, rowTransformation)
                    color = QColor(0, 0, 0)  # set the color is unspecified

                    if self.boardArray[col][row] == Piece.NoPiece:  # if piece in array == 0
                        color = QColor(Qt.transparent)  # color is transparent

                    elif self.boardArray[col][row]== Piece.White:  # if piece in array == 1
                        color = QColor(Qt.white)  # set color to white

                    elif self.boardArray[col][row] == Piece.Black:  # if piece in array == 2
                        color = QColor(Qt.black)  # set color to black

                    painter.setPen(color)  # set pen color to painter
                    painter.setBrush(color)  # set brush color to painter
                    painter.translate(self.squareWidth(), self.squareHeight())
                    radius = int((self.squareWidth() - 2) / 2)
                    center = QPoint(col, row)
                    if (row == Board.boardWidth or col == Board.boardHeight):
                        pass
                    else:
                        painter.drawEllipse(center, radius, radius)
                    painter.restore()

    def placePiece(self,painter):
        # Calculate the radius of the circle
        radius = min(self.squareWidth(), self.squareHeight()) / 4

        # Draw the circle on top of the top-left corner of the box
        painter.setBrush(QBrush(QColor(255, 0, 0)))  # Set brush color to red (you can choose your color)
        painter.drawEllipse(int(self.posX), int(self.posY), int(2 * radius), int(2 * radius))

