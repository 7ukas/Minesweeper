from collections import namedtuple
from Difficulty import Difficulty
from Cell import Cell
from Status import Status
import random

class Minesweeper:
    # Coordinates
    Point = namedtuple('Point', ['y', 'x'])

    # Board
    _board = dict()
    _solved_board = dict()

    _max_height = 0
    _max_width = 0
    _max_mines = 0

    # Game Properties
    _game_active = True
    _status = Status.UNKNOWN
    _flagged_count = 0

    def __init__(self, difficulty):
        difficulty = Difficulty(difficulty)
        self._max_height = difficulty.height()
        self._max_width = difficulty.width()
        self._max_mines = difficulty.mines()

        # Create new empty cells for both boards
        for y in range(self._max_height):
            for x in range(self._max_width):
                print('{0} : {1}'.format(y, x))
                self._solved_board.update({self.Point(y,x):Cell(0)})
                self._board.update({self.Point(y,x):Cell(-2)})

        self._generate()

    def _generate(self):
        # Planting mines
        mines_planted = 0
        while mines_planted < self._max_mines:
            y = random.randint(0, self._max_height - 1)
            x = random.randint(0, self._max_width - 1)

            if not self._get_cell(y,x).is_mined():
                mines_planted = mines_planted + 1
                self._get_cell(y,x).mine()

        # Setting values (numbers)
        for y in range(self._max_height):
            for x in range(self._max_width):
                cell = self._get_cell(y,x)

                if cell.is_mined():
                    continue

                if y > 0 and self._get_cell(y-1,x).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if y < self._max_height - 1 and self._get_cell(y+1,x).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if x > 0 and self._get_cell(y,x-1).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if x < self._max_width - 1 and self._get_cell(y,x+1).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if y > 0 and x > 0 and self._get_cell(y-1,x-1).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if y > 0 and x < self._max_width - 1 and self._get_cell(y-1,x+1).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if y < self._max_height - 1 and x > 0 and self._get_cell(y+1,x-1).is_mined():
                    cell.set_value(cell.get_value() + 1)
                if y < self._max_height - 1 and x < self._max_width - 1 and self._get_cell(y+1,x+1).is_mined():
                    cell.set_value(cell.get_value() + 1)

        self._status = Status.READY

    def _uncover_neighbours(self, y, x):
        solved_cell = self._get_cell(y,x)
        cell = self._board.get(self.Point(y,x))

        if not solved_cell.is_visited():
            solved_cell.visit()
            cell.set_value(solved_cell.get_value())

            if cell.is_flagged():
                self._flagged_count = self._flagged_count - 1

            if cell.get_value() == 0:
                if y > 0:
                    self._uncover_neighbours(y-1, x)
                if y < self._max_height-1:
                    self._uncover_neighbours(y+1, x)
                if x > 0:
                    self._uncover_neighbours(y, x-1)
                if x < self._max_width-1:
                    self._uncover_neighbours(y, x+1)
                if y > 0 and x > 0:
                    self._uncover_neighbours(y-1, x-1)
                if y > 0 and x < self._max_width-1:
                    self._uncover_neighbours(y-1, x+1)
                if y < self._max_height-1 and x > 0:
                    self._uncover_neighbours(y+1, x-1)
                if y < self._max_height-1 and x < self._max_width-1:
                    self._uncover_neighbours(y+1, x+1)

    def _get_cell(self, y, x):
        return self._solved_board.get(self.Point(y, x))

    def _get_mines(self):
        return [k for k, v in self._solved_board.items() if v.is_mined()]

    def _get_visited_cells(self):
        return [k for k, v in self._solved_board.items() if v.is_visited()]

    # Left Mouse Button
    def uncover_cell(self, y, x):
        if self._status == Status.READY:
            self._status = Status.ACTIVE

        cell = self._get_cell(y,x)

        # Clicked: Mine (Lost)
        if cell.is_mined():
            for mine in self._get_mines():
                self._board.get(self.Point(mine.y, mine.x)).set_value(-1)
            self._game_active = False
            self._status = Status.LOST

        # Clicked: 0
        elif cell.get_value() == 0:
            for key in self._get_visited_cells():
                self._get_cell(key.y, key.x).unvisit()
            self._uncover_neighbours(y, x)

        # Clicked: 1-8
        else:
            self._board.get(self.Point(y,x)).set_value(cell.get_value())
            if len([k for k, v in self._board.items() if v.is_covered()]) == self._max_mines:
                self._status = Status.WON

    # Right Mouse Button
    def flag_cell(self, y, x):
        if self._status == Status.READY:
            self._status = Status.ACTIVE

        cell = self._board.get(self.Point(y,x))

        if not cell.is_flagged():
            cell.flag()
            self._flagged_count = self._flagged_count + 1
        else:
            cell.unflag()
            self._flagged_count = self._flagged_count - 1

    def height(self):
        return self._max_height

    def width(self):
        return self._max_width

    def mines(self):
        return self._max_mines

    def flagged_count(self):
        return self._flagged_count

    def get_board(self):
        return self._board

    def get_solved_board(self):
        return self._solved_board

    def status(self):
        return self._status