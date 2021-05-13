import numpy
from enum import Enum


class MapCell(Enum):
    EMPTY = 1
    OBSTACLE = 2


class Map(object):
    def __init__(self):
        self.__n = 0
        self.__m = 0
        self.__surface: numpy.matrix = None

    @property
    def n(self):
        return self.__n

    @property
    def m(self):
        return self.__m

    @property
    def surface(self):
        return self.__surface

    @n.setter
    def n(self, value):
        self.__n = value

    @m.setter
    def m(self, value):
        self.__m = value

    @surface.setter
    def surface(self, value):
        self.__surface = value

    def load_from_binary_file(self):


    def get_cell_value(self, coord_i, coord_j):
        if 0 <= coord_i <= self.__n and 0 <= coord_j <= self.__m:
            return self.__surface[coord_j][coord_j]
