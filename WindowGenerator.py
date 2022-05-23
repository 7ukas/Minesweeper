from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Minesweeper import Minesweeper
from Status import Status
from Difficulty import Difficulty

import time
import sys

class MainWindow(QMainWindow):
    def __init__(self, difficulty):
        super().__init__()

        # Minesweeper
        self.difficulty = difficulty
        self.minesweeper = Minesweeper(difficulty)
        self.solved_board = self.minesweeper.get_solved_board()

        self.MAX_HEIGHT = self.minesweeper.height()
        self.MAX_WIDTH = self.minesweeper.width()
        self.MAX_MINES = self.minesweeper.mines()

        # PyQt
        self.buttons = []
        self.difficulty_buttons = []
        self.reset_button = None
        self.mines_label = None

        self.stopwatch_label = None
        self.stopwatch_running = False
        self.stopwatch_time = 0

        # Font in (Mines, Stopwatch)
        font = QFont("Arial")
        font.setWeight(70)
        font.setPointSize(23)

        # Mines in Scoreboard - HBox
        self.mines_label = QLabel()
        self.mines_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mines_label.setFont(font)
        self.mines_label.setText('%03d' % self.MAX_MINES)

        mines_image = QFrame()
        mines_image.setObjectName('mine')
        mines_image.setFixedSize(35,35)

        mines_hbox = QHBoxLayout()
        mines_hbox.addWidget(mines_image)
        mines_hbox.addWidget(self.mines_label)

        # Reset in Scoreboard - PushButton
        self.reset_button = QPushButton()
        self.reset_button.setFixedSize(QSize(45, 45))
        self.reset_button.setIconSize(QSize(45, 45))
        self.reset_button.setIcon(QIcon("images/alive.png"))
        self.reset_button.setFlat(True)
        self.reset_button.pressed.connect(self.reset)

        # Stopwatch in Scoreboard - HBox
        self.stopwatch_label = QLabel()
        self.stopwatch_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stopwatch_label.setFont(font)
        self.stopwatch_label.setText("000")

        stopwatch_image = QFrame()
        stopwatch_image.setObjectName('stopwatch')
        stopwatch_image.setFixedSize(37,37)

        stopwatch_hbox = QHBoxLayout()
        stopwatch_hbox.addWidget(self.stopwatch_label)
        stopwatch_hbox.addWidget(stopwatch_image)

        self.stopwatch = QTimer()
        self.stopwatch.timeout.connect(self.update_stopwatch)

        # Font in (Difficulties)
        font = QFont("Calibri")
        font.setPointSize(12)

        # Difficulty Buttons - PushButton
        for n in range(1,4):
            button = QPushButton()
            button.setObjectName('difficulty%d' % n)
            button.setFont(font)
            button.setText(Difficulty(n).name())
            button.setFixedHeight(32)
            button.pressed.connect(self.change_difficulty)
            self.difficulty_buttons.append(button)

        self.difficulty_buttons[0].setFixedWidth(72)
        self.difficulty_buttons[1].setFixedWidth(98)
        self.difficulty_buttons[2].setFixedWidth(58)
        self.difficulty_buttons[2].setDisabled(True)

        # Scoreboard (Mines, Reset, Stopwatch) - HBox
        scoreboard_hbox = QHBoxLayout()
        scoreboard_hbox.setSpacing(10)
        scoreboard_hbox.setContentsMargins(5, 5, 5, 5)
        scoreboard_hbox.addLayout(mines_hbox)
        scoreboard_hbox.addStretch(1)
        scoreboard_hbox.addWidget(self.reset_button)
        scoreboard_hbox.addStretch(1)
        scoreboard_hbox.addLayout(stopwatch_hbox)

        # Board - GridLayout
        board_grid = QGridLayout()
        board_grid.setSpacing(0)
        board_grid.setContentsMargins(0, 0, 0, 0)

        # Difficulties - HBox
        difficulties_hbox = QHBoxLayout()
        difficulties_hbox.setSpacing(10)
        difficulties_hbox.setContentsMargins(5, 5, 5, 5)
        difficulties_hbox.addWidget(self.difficulty_buttons[0])
        difficulties_hbox.addStretch(1)
        difficulties_hbox.addWidget(self.difficulty_buttons[1])
        difficulties_hbox.addStretch(1)
        difficulties_hbox.addWidget(self.difficulty_buttons[2])

        # Create Grid - PushButton
        for y in range(self.MAX_HEIGHT):
            for x in range(self.MAX_WIDTH):
                button = QPushButton()
                button.setFlat(True)
                button.setFixedSize(QSize(30, 30))
                button.setIconSize(QSize(30, 30))
                button.setIcon(QIcon(QIcon('images/covered.png')))
                button.setObjectName('cell@y%02d:x%02d' % (y, x))
                button.installEventFilter(self)

                self.buttons.append(button)
                board_grid.addWidget(button, y, x)

        # (Scoreboard, Board) in VBox
        vbox = QVBoxLayout()

        frame = QFrame()
        frame.setLayout(scoreboard_hbox)
        vbox.addWidget(frame)

        frame = QFrame()
        frame.setLayout(board_grid)
        vbox.addWidget(frame)

        frame = QFrame()
        frame.setLayout(difficulties_hbox)
        vbox.addWidget(frame)

        # MainWindow
        widget = QWidget()
        widget.setLayout(vbox)

        if difficulty == Difficulty.BEGINNER:
            self.setFixedSize(298, 430)
        elif difficulty == Difficulty.INTERMEDIATE:
            self.setFixedSize(508, 639)

        self.setCentralWidget(widget)
        self.setWindowTitle('Minesweeper: %s (%dx%d)' % (Difficulty(difficulty).name(), self.MAX_HEIGHT, self.MAX_WIDTH))

    def eventFilter(self, obj, event):
        if self.minesweeper.status() in [Status.ACTIVE, Status.READY]:
            if event.type() == QEvent.MouseButtonPress:
                # Start stopwatch
                if not self.stopwatch_running:
                    self.stopwatch_time = time.time()
                    self.stopwatch.start(500)
                    self.stopwatch_running = True

                name = obj.objectName()
                pos = Minesweeper.Point(int(name[6:8]), int(name[10:12]))
                cell = self.minesweeper.get_board().get(pos)

                # Left Mouse Button - Event
                if event.button() == Qt.LeftButton:
                    if not cell.is_flagged():
                        self.minesweeper.uncover_cell(pos.y, pos.x)
                        status = self.minesweeper.status()
                        board = self.minesweeper.get_board()
                        cell = board.get(pos)

                        self.mines_label.setText('%03d' % int(self.MAX_MINES - self.minesweeper.flagged_count()))

                        # In case the game was WON or LOST
                        if status in [Status.WON, Status.LOST]:
                            self.stopwatch_running = False

                            if status == Status.WON:
                                self.reset_button.setIcon(QIcon("images/won.png"))
                                self.mines_label.setText('000')
                            elif status == Status.LOST:
                                self.reset_button.setIcon(QIcon("images/lost.png"))
                                uncovered_mines = self.MAX_MINES - len(list(filter(lambda x: x.is_mined() and x.is_flagged(),
                                                                  self.minesweeper.get_board().values()))) - 1
                                self.mines_label.setText('%03d' % uncovered_mines)

                        # Clicked: 0-8
                        if not cell.is_mined():
                            for y in range(self.MAX_HEIGHT):
                                for x in range(self.MAX_WIDTH):
                                    temp_cell = board.get(Minesweeper.Point(y, x))

                                    if not temp_cell.is_covered():
                                        self.buttons[self._index(y, x)].setIcon(
                                            QIcon('images/%d.png' % temp_cell.get_value()))
                        # Clicked: Mine (Lost)
                        else:
                            for y in range(self.MAX_HEIGHT):
                                for x in range(self.MAX_WIDTH):
                                    temp_cell = board.get(Minesweeper.Point(y, x))
                                    img_url = ''

                                    if temp_cell.is_mined() and temp_cell.is_flagged():
                                        img_url = 'images/flagged.png'
                                    elif temp_cell.is_mined() and not temp_cell.is_flagged():
                                        img_url = 'images/mine.png'
                                    elif not temp_cell.is_mined() and temp_cell.is_flagged():
                                        img_url = 'images/flagged_falsely.png'
                                    elif temp_cell.is_covered():
                                        img_url = 'images/covered.png'
                                    elif not temp_cell.is_covered():
                                        img_url = 'images/%d.png' % temp_cell.get_value()

                                    self.buttons[self._index(y, x)].setIcon(QIcon(img_url))

                            self.buttons[self._index(pos.y, pos.x)].setIcon(QIcon('images/mine_exploded.png'))

                # Right Mouse Button - Event
                elif event.button() == Qt.RightButton:
                    if cell.is_covered():
                        self.minesweeper.flag_cell(pos.y, pos.x)
                        cell = self.minesweeper.get_board().get(pos)

                        img_url = 'images/flagged.png' if cell.is_flagged() else 'images/covered.png'
                        self.buttons[self._index(pos.y, pos.x)].setIcon(QIcon(img_url))
                        self.mines_label.setText('%03d' % int(self.MAX_MINES - self.minesweeper.flagged_count()))

        return QObject.event(obj, event)

    # Reset the game
    def reset(self):
        status = self.minesweeper.status()
        if status in [Status.ACTIVE, Status.WON, Status.LOST]:
            self.minesweeper = Minesweeper(self.difficulty)
            self.solved_board = self.minesweeper.get_board()
            self.sender().setIcon(QIcon("images/alive.png"))
            self.mines_label.setText('%03d' % self.MAX_MINES)

            self.stopwatch_running = False
            self.stopwatch_label.setText('000')

            for button in self.buttons:
                button.setIcon(QIcon(QIcon('images/covered.png')))

    # Keep stopwatch running
    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_label.setText('%03d' % (time.time() - self.stopwatch_time))

    # Makes new game with new difficulty attached
    def change_difficulty(self):
        difficulty = self.sender().text()

        self.close()

        if difficulty == "Beginner":
            self.__init__(Difficulty.BEGINNER)
        elif difficulty == "Intermediate":
            self.__init__(Difficulty.INTERMEDIATE)
        elif difficulty == "Expert":
            self.__init__(Difficulty.EXPERT)

        self.show()

    def _index(self, y, x):
        return (y * self.MAX_HEIGHT) + x


stylesheet = """
    QWidget {
        background-color: #D4D4D4;
    }
    
    QFrame {
        border: 5px inset #757575; 
        padding: 0;
    }
    
    QFrame#mine {
        background-image: url('images/mine_transparent.png');
        border: 0
    }
    
    QFrame#stopwatch {
        background-image: url('images/stopwatch_transparent.png');
        border: 0
    }
    
    QLabel {
        color: #FF2E2E;
        border: 0;
    }
    
    QPushButton#difficulty1, #difficulty2, #difficulty3 {
        border: 3px outset #757575;
    }
"""

app = QApplication(sys.argv)
app.setStyleSheet(stylesheet)
window = MainWindow(1)
window.show()
app.exec()
