from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt

from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        self.board = Board(self)
        self.setCentralWidget(self.board)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.createStatusBar()  # Added this line to create a status bar
        self.setFixedSize(650,650)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def createStatusBar(self):
        statusbar = self.statusBar()
        statusbar.showMessage('Ready')  # Initial status message

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
