import random
from src.utils.variables import *


class Gene(object):
    def __init__(self):
        self.coords: Coords = Coords()
        self.from_direction: int = 0

    def random(self, previous_cell: Coords, available_directions: list):
        self.from_direction = random.randint(0, len(available_directions) - 1)
        self.coords = previous_cell + DIRECTIONS[available_directions[self.from_direction]]
        return self.coords
