class Difficulty:
    BEGINNER = 1
    INTERMEDIATE = 2
    EXPERT = 3

    _name = ''
    _height = 0
    _width = 0
    _mines = 0

    def __init__(self, difficulty):
        if difficulty == Difficulty.BEGINNER:
                self._name = 'Beginner'
                self._height = 9
                self._width = 9
                self._mines = 10
        elif difficulty == Difficulty.INTERMEDIATE:
                self._name = 'Intermediate'
                self._height = 16
                self._width = 16
                self._mines = 40
        elif difficulty == Difficulty.EXPERT:
                self._name = 'Expert'
                self._height = 16
                self._width = 36
                self._mines = 99

    def name(self):
        return self._name

    def height(self):
        return self._height

    def width(self):
        return self._width

    def mines(self):
        return self._mines