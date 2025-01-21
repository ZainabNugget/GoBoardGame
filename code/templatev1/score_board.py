from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSlot

from code.templatev1.game_logic import GameLogic



class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    gameLogic = GameLogic()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(100, 200)
        self.setWindowTitle('ScoreBoard')
        self.setStyleSheet('''
            background-color: #808080
        ''')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # TODO Create labels for each of the following:
        self.label_instructions = QLabel("Instructions"
                                         "\n 1. Click any where to start"
                                         "\n 2. Press 'Pass' to pass turn"
                                         "\n 3. Press 'Reset' to reset the Game"
                                         "\n Rules:"
                                         "\n 1. A player can only pass once,"
                                         "\n After two passes, the game ends")
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_notification = QLabel("")
        self.label_currentplayer = QLabel("Current player: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        # White
        self.label_whiteprisoners = QLabel("White prisoners: ")
        self.label_whiteterritories = QLabel("White Territory: ")

        # Black
        self.label_blackprisoners = QLabel("Black prisoners: ")
        self.label_blackterritories = QLabel("Black Territory: ")

        # Undo/Redo Buttons
        self.undo = QPushButton("Undo")
        self.redo = QPushButton("Redo")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.undo)
        self.hbox.addWidget(self.redo)

        # buttons in score board
        self.passBtn = QPushButton("Pass")
        self.resetBtn = QPushButton("Reset")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_instructions)
        # self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_notification)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_currentplayer)

        # Add undo, redo buttons
        self.mainLayout.addLayout(self.hbox)

        # White player scores
        self.mainLayout.addWidget(self.label_whiteprisoners)
        self.mainLayout.addWidget(self.label_whiteterritories)

        # Black player scores
        self.mainLayout.addWidget(self.label_blackprisoners)
        self.mainLayout.addWidget(self.label_blackterritories)

        self.mainLayout.addWidget(self.passBtn)
        self.mainLayout.addWidget(self.resetBtn)

        self.setWidget(self.mainWidget)

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)  # shows the click locations
        board.updateTimerSignal.connect(self.setTimeRemaining)   # displays time remaining, countdown
        board.displayTurn.connect(self.updateturn)  # change the turn displayed after the turn is updated
        board.updatePrisoners.connect(self.updatePrisoners)  # updates prisoners count for both players
        board.updateTerritories.connect(self.updateTerritory)  # update territories
        board.showNotificationSignal.connect(self.updateNotification)  # update notifications
        self.passBtn.clicked.connect(board.passTurn)  # connects to a method from board
        self.resetBtn.clicked.connect(board.resetGame)  # connects to a method to reset the game
        self.undo.clicked.connect(board.undo)  # connects to an undo method from board
        self.redo.clicked.connect(board.redo)  # connects to a redo method from board

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        # print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeremaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeremaining)
        self.label_timeRemaining.setText(update)
        # print('slot ' + str(timeRemaining))
        # self.redraw()

    # TODO change the turn display
    def updateturn(self, Piece):   # Updates the turn displayed
        if (Piece == 1):
            self.label_currentplayer.setText("Current Turn: White")
        elif (Piece == 2):
            self.label_currentplayer.setText("Current Turn: Black")

    # TODO Implement the update prisoners text(setText based on current player)
    def updatePrisoners(self, white, black):
        whiteStr = "White's prisoners: " + str(white)
        blackStr = "Black's prisoners: " + str(black)
        self.label_whiteprisoners.setText(whiteStr)
        self.label_blackprisoners.setText(blackStr)

    # TODO Implement the update territories text(setText based on territories (black/white))
    def updateTerritory(self, white, black):
        whiteStr = "White territories amount to: " + str(white)
        blackStr = "Black territories amount to: " + str(black)
        self.label_whiteterritories.setText(whiteStr)
        self.label_blackterritories.setText(blackStr)

    # TODO Update the notifications
    def updateNotification(self, text):
        self.label_notification.setText(text)
