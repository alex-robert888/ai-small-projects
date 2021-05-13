class Coords(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
