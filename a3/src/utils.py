# -*- coding: utf-8 -*-

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3


class Coords(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __add__(self, other):
        return Coords(self.i + other.i, self.j + other.j)


#define indexes variations 
DIRECTIONS = [Coords(-1, 0), Coords(1, 0), Coords(0, 1), Coords(0, -1)]

#define mapsize 

mapLengh = 20