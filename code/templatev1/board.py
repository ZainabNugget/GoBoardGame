from PyQt6.QtWidgets import QFrame, QMessageBox
from PyQt6.QtCore import QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    displayTurn = pyqtSignal(int)  # signal sent to update display of the current player
    updateTerritories = pyqtSignal(int, int)  # signal sent to update territories
    updatePrisoners = pyqtSignal(int, int)  # signal sent to update prisoner number
    showNotificationSignal = pyqtSignal(str)  # signal sent for notification message.

    # TODO set the board width and height to be square
    boardWidth = 7  # board width will be 7 squares
    boardHeight = 7  # board height will be 7 squares

    timerSpeed = 1000  # the timer updates every 1 second
    counter = 120  # the number the counter will count down from
    posX = 0  # x position of mouse click
    posY = 0  # y position of mouse click

    previousX = 0
    previousY = 0

    previous_board = []
    board_hist = []
    undo_history = []
    redo_move = []

    playerPassCount = 0

    gameLogic = GameLogic()  # Init game logic object

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.setStyleSheet('''
        background-color: #5e3f20
        ''')
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        # TODO - create a 2d int/Piece array to store the state of the game
        rows, cols = (7, 7)
        self.boardArray = [[Piece.NoPiece] * cols for _ in range(rows)]
        self.gameLogic.boardArray = self.boardArray
        self.copy_board()

        self.printBoardArray()  # TODO - uncomment this method after creating the array above

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

        if (col <= 0): col = 1
        if (row <= 0): row = 1

        if (col >= 7): col = 7
        if (row >= 7): row = 7

        row -= 1
        col -= 1

        if self.tryMove(row, col):  # check for suicide and for vacancy
            self.placePiece(row, col)  # place the piece on the board
            strin = "Placed a move at row" + str(row) + " col " + str(col)
            self.undo_history.append([row, col])  # use the history in board to return the move
            self.redo_move = []  # clear the redo history
            print(self.undo_history)
            self.showNotificationSignal.emit(strin)

        self.gameLogic.updateScores()
        self.update()

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / 8

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / 8

    '''
    Message popup to declare the winner
    '''
    def playerWon(self):
        if (self.gameLogic.currentPlayer == Piece.Black):
            QMessageBox.information(self, "Game Over", "Black Lost!")
        else:
            QMessageBox.information(self, "Game Over", "White Lost!")

    '''
    - When the counter is 0, declare a winner
    - When there is a new player, we reset the counter
    to 120s
    '''
    def timerEvent(self):
        if self.counter == 0:
            self.endGame()
            self.winner()
        else:
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)

    def start(self):
        '''starts game'''
        self.isStarted = True
        self.resetGame()
        self.timer.start(self.timerSpeed)
        print("start () - timer is started")
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        x = event.position().x()  # x position of mouse click
        y = event.position().y()  # y position of mouse click
        self.posX = event.position().x()
        self.posY = event.position().y()
        clickLoc = f"Click location: [{x}, {y}]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.mousePosToColRow(event)  # a method that converts the mouse click to a row and col.
        self.clickLocationSignal.emit(clickLoc)

    '''
    To end the game
    - Reset game
    - Stop timers
    - Declare winner
    '''
    def endGame(self):
        self.isStarted = False
        self.resetGame()
        self.timer.stop()
        self.winner()
        self.showNotificationSignal.emit("Game's Over!")
    '''
    To reset the game:
    - Clear the array
    - Change the player to Black
    - reset all scores 
    - update the program
    '''
    def resetGame(self):  # resets the game by clearing the array and resetting the player
        '''clears pieces from the board'''
        # TODO write code to reset game
        self.boardArray = [[Piece.NoPiece for self.boardHeight in range(7)] for self.boardWidth in range(7)]
        self.gameLogic.currentPlayer = Piece.Black

        # Reset all scores
        self.undo_history = []
        self.redo_move = []
        self.gameLogic.capturedBlack = 0
        self.gameLogic.capturedWhite = 0
        self.gameLogic.whiteTerritory = 0
        self.gameLogic.blackTerritory = 0
        self.update()
        print("Game was reset.")

    # TODO Win conditions
    '''
    Get the winner based on the higher score
    '''
    def winner(self):  # compare scores and give a winner!
        if self.gameLogic.whiteScore > self.gameLogic.blackScore:
            self.winDeclaration(Piece.White)
            self.showNotificationSignal.emit("White is the winner!")
        elif self.gameLogic.whiteScore < self.gameLogic.blackScore:
            self.winDeclaration(Piece.Black)
            self.showNotificationSignal.emit("Black is the winner!")
        else:
            self.showNotificationSignal.emit("It's a Tie!")
        print(self.gameLogic.whiteScore, self.gameLogic.blackScore)

    def winDeclaration(self, player):
        if (player == Piece.Black):
            QMessageBox.information(self, "Game Over", "Black Won!")
        else:
            QMessageBox.information(self, "Game Over", "White Won!")
    '''
    Before a piece is placed:
    - Check if the spot is empty
    - Check for suicide
    '''
    def tryMove(self, row, col):  # does the necessary checks for placing a stone
        '''tries to move a piece'''
        if self.gameLogic.checkEmpty(row, col):
            if self.gameLogic.suicideRule(row, col):
                self.showNotificationSignal.emit("This move is suicide!")
                return False
            return True
        else:  # Implement this method according to your logic
            self.showNotificationSignal.emit("Illegal Move.")
            return False

    '''
    The undo and redo method uses stacks
    Undo:
    - add in previous moves, whenever a move is done
    - add it to a redo history stack in case of a redo
    - update turn to go back to the original player
    - update the program, to reprint the piece
    '''
    def undo(self):
        if self.undo_history:  # checks if there are any in the history
            row, col = self.undo_history.pop()  # get the first element and reverse
            self.redo_move.append([row, col, self.gameLogic.currentPlayer])
            self.boardArray[row][col] = Piece.NoPiece  # clear the spot
            self.gameLogic.updateTurn()  # return to the other player
            self.displayTurn.emit(self.gameLogic.currentPlayer)  # change the display
            self.update()  # update the program
        else:
            self.showNotificationSignal.emit("No history to undo from!")
    '''
    Redo:
    - take the first row, col from the stack
    - add the previous player to the row,col
    - update turn to move to the next player
    - update the program to print the piece
    '''
    def redo(self):
        if self.redo_move:
            row, col, player= self.redo_move.pop()
            if player == Piece.Black:
                player = Piece.White
            else:
                player = Piece.Black
            self.boardArray[row][col] = player
            self.gameLogic.updateTurn()
            self.displayTurn.emit(self.gameLogic.currentPlayer)  # change the display
            self.update()
        else:
            self.showNotificationSignal.emit("No redo history!")

    def drawBoardSquares(self, painter):  # Creates the general board layout of the game
        '''draw all the square on the board'''
        # setting the default colour of the brush
        brush = QBrush(Qt.SolidPattern)  # calling SolidPattern to a variable
        brush.setColor(QColor(245, 173, 66))  # setting color to orange
        painter.setBrush(brush)  # setting brush color to painter

        for row in range(1, Board.boardHeight + 1):
            for col in range(1, Board.boardWidth + 1):
                painter.save()
                # Set the Col and Row values
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)

                # Skips the extra boxes we dont need
                if (row == Board.boardHeight or col == Board.boardWidth):
                    pass
                else:
                    painter.fillRect(col, row, int(self.squareWidth()), int(self.squareHeight()), brush)
                # Make small circles
                radius = int((10 - 2) / 2)
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

                # Changing the colour of the brush so that a slightly different colored board is drawn
                if brush.color() == QColor(245, 173, 66):
                    brush.setColor(QColor(237, 171, 71))
                else:
                    brush.setColor(QColor(245, 173, 66))

    def drawPieces(self, painter):  # paints the pieces based on the board array
        '''draw the pieces on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                # # TODO draw some pieces as ellipses
                # # TODO choose your color and set the painter brush to the correct color
                if not Piece.NoPiece:
                    painter.save()
                    colTransformation = self.squareWidth() * col
                    rowTransformation = self.squareHeight() * row
                    painter.translate(colTransformation, rowTransformation)
                    color = QColor(0, 0, 0)  # set the color is unspecified

                    if self.boardArray[row][col] == Piece.NoPiece:  # if piece in array == 0
                        color = QColor(0, 20, 20)  # color is transparent
                    elif self.boardArray[row][col] == Piece.White:  # if piece in array == 1
                        color = QColor(255, 255, 255)  # set color to white
                    elif self.boardArray[row][col] == Piece.Black:  # if piece in array == 2
                        color = QColor(0, 0, 0)  # set color to black

                    painter.setPen(color)  # set pen color to painter
                    painter.setBrush(color)  # set brush color to painter
                    painter.translate(self.squareWidth(), self.squareHeight())
                    radius = int((40 - 2) / 2)
                    center = QPoint(col, row)
                    if (row == Board.boardWidth or col == Board.boardHeight or self.boardArray[row][
                        col] == Piece.NoPiece):
                        pass
                    else:
                        painter.drawEllipse(center, radius, radius)
                    painter.restore()
                    self.update()

    '''
    The logic behind placing a piece
    - updates the array 
    - updates the territory scores 
    - updates the turn 
    - resets timer for the player 
    - updates any captures that happen
    - updates the prisoners score
    '''
    def placePiece(self, row, col):

        # Enter based on the current player
        self.previous_board = self.copy_board()  # copy the board into the previous board var
        self.gameLogic.updateArray(row, col)
        self.gameLogic.updateTerritory()
        self.updateTerritories.emit(self.gameLogic.whiteTerritory, self.gameLogic.blackTerritory)
        # Update everything after successful placement
        self.gameLogic.updateTurn()

        print("Black captured: ", self.gameLogic.capturedBlack)
        print("White captured: ", self.gameLogic.capturedWhite)

        self.resetCounter()
        # Update timers and turn
        self.displayTurn.emit(self.gameLogic.currentPlayer)
        self.updateTimerSignal.emit(self.counter)

        # Print both arrays
        self.printBoardArray()

        # copy the board history into an array
        self.board_history()
        self.gameLogic.capture()
        self.gameLogic.captureMultiple()
        self.updatePrisoners.emit(self.gameLogic.capturedWhite, self.gameLogic.capturedBlack)
        self.update()

    def resetCounter(self):
        self.counter = 120

    # TODO implement pass rule
    '''
    After either player passes a turn
    if the count is 2, we end the game!
    '''
    def passTurn(self):  # update the turn and increment count based on player
        self.playerPassCount += 1
        print(self.playerPassCount)
        if self.playerPassCount >= 2:
            self.endGame()
            self.winner()
            self.update()
        self.gameLogic.updateTurn()
        self.displayTurn.emit(self.gameLogic.currentPlayer)

    '''
    We attempted to create the KO rule, however,
    our attempt was a failure and so we decided
    not to include it in the final project, the
    idea behind this code, is that there would be 
    a copy of the board made, before a move is made
    the ko method then checks if the current board
    is equal to the previous board
    
    '''

    def copy_board(self):
        ''' A method to store and return the current state of the board '''
        rows, cols = (7,7)
        copy_board = [[Piece.NoPiece] * cols for _ in range(rows)] # nested loop of Stone class to the size of board range.
        rowindex = 0
        for row in self.boardArray:
            colindex = 0
            for cell in row:
                if cell == Piece.White:
                    copy_board[rowindex][colindex] = Piece.White # places the current value of white stone to the copyofboard row and col index
                elif cell == Piece.Black:
                    copy_board[rowindex][colindex] = Piece.Black # places the current value of black stone to the copyofboard row and col index
                else:
                    pass
                colindex = colindex + 1  # increment col index
            rowindex = rowindex + 1  # increment row index
        return copy_board

    def board_history(self):
        self.board_hist.append(self.copy_board())
        print(self.board_hist)

    def ko(self, row, col):
        temp_board = [row.copy() for row in self.boardArray]
        temp_board[row][col] = self.gameLogic.currentPlayer

        return self.previous_board == temp_board
