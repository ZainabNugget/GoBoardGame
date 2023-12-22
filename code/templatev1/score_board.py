from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot, Qt

from code.templatev1.board import Board
from code.templatev1.game_logic import GameLogic
from code.templatev1.piece import Piece


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    gameLogic = GameLogic()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_instructions = QLabel("Instructions\n 1. Click any where to place\n a piece \n 2. Press P to pass a turn \n 3. Press R to reset the Game")
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_currentplayer = QLabel("Current player: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.label_whiteprisoners = QLabel("White prisoners: ")
        self.label_blackprisoners = QLabel("Black prisoners: ")
        self.label_whiteterritories = QLabel("White prisoners: ")
        self.label_blackterritories = QLabel("Black prisoners: ")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_instructions)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_currentplayer)
        self.setWidget(self.mainWidget)

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        # change the turn displayed after the turn is updated
        board.displayTurn.connect(self.updateturn)
        # update territories
        board.updateTerritories.connect(self.updateTerritory)

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

    # Updates the turn displayed
    def updateturn(self, Piece):
        if (Piece == 1):
            self.label_currentplayer.setText("Current Turn: White")
        elif (Piece == 2):
            self.label_currentplayer.setText("Current Turn: Black")

    # TODO Implement the update prisoners text(setText based on current player)
    def updatePrisoners(self):
       self.label_whiteprisoners.setText("White prisoners captured: ")
       self.label_blackprisoners.setText("Black prisoners captured: ")

    # TODO Implement the update territories text(setText based on territories (black/white))
    def updateTerritory(self):
        self.label_whiteterritories.setText("White territories amount to: ")
        self.label_blackterritories.setText("Black territories amount to: ")

