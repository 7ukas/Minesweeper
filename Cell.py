class Cell:
    _visited = False
    _flagged = False
    _covered = False
    _mined = False
    _value = 0         # -2: Covered/Empty, -1: Mine, 0=< Number

    def __init__(self):
        self.set_value(-2)

    def __init__(self, value):
        self.set_value(value)

    def flag(self): self._flagged = True
    def unflag(self): self._flagged = False
    def is_flagged(self): return self._flagged

    def visit(self): self._visited = True
    def unvisit(self): self._visited = False
    def is_visited(self): return self._visited

    def cover(self): self._covered = True
    def uncover(self): self._covered = False
    def is_covered(self): return self._covered

    def mine(self): self._mined = True
    def demine(self): self._mined = False
    def is_mined(self): return self._mined

    def set_value(self, value):
        if type(value) is int:
            self._value = value
            self._covered = True if value == -2 else False
            self._mined = True if value == -1 else False

    def get_value(self):
        return self._value

    def to_string(self):
        return '[Value: %d, Mined: %r, Flagged: %r, Covered: %r, Visited: %r]' % \
               (self._value, self._mined, self._flagged, self._covered, self._visited)