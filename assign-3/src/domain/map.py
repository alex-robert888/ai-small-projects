import numpy
import pickle
from enum import Enum
from src.domain.coords import Coords
from src.utils.variables import *
from src.utils.config import *


class MapCell(Enum):
    EMPTY = 1
    OBSTACLE = 2


class Map(object):
    def __init__(self):
        self.n = 0
        self.m = 0
        self.surface: numpy.matrix = None
        self.__starting_coords = Coords()
        self.__available_directions = []
        self.__visited = []
        self.__how_many_visited = 0

    def get_cell_value(self, coords):
        if 0 <= coords.x <= self.n and 0 <= coords.y <= self.m:
            return self.surface[coords.y][coords.x]

    def get_starting_coords(self):
        return self.__starting_coords

    def get_available_directions_for_cell(self, coords: Coords):
        return self.__available_directions[coords.y][coords.x]

    def is_valid_cell(self, coords: Coords):
        return 0 <= coords.x < self.n and 0 <= coords.y < self.m and self.surface[coords.y, coords.x] == 0

    def load_from_binary_file(self, map_file_path: str):
        with open(map_file_path, "rb") as f:
            loaded_map = pickle.load(f)
            self.n = loaded_map.n
            self.m = loaded_map.m
            self.surface = loaded_map.surface
            print("---- surface")
            for x in range(self.n):
                for y in range(self.m):
                    print(self.surface[y][x], end=' ')
                print()
            print("---- surface")
            self.__starting_coords = Coords(STARTING_COORDS_X, STARTING_COORDS_Y)
            self.__precompute_available_directions_for_each_cell()

    def init_exploring(self):
        self.__visited = [[False for x in range(self.m)] for y in range(self.n)]
        self.__how_many_visited = 0

    def explore(self, coords):
        for direction in DIRECTIONS:
            copy_coords = Coords(coords.x, coords.y) + direction
            while self.is_valid_cell(copy_coords):
                if not self.__visited[copy_coords.y][copy_coords.x]:
                    self.__how_many_visited += 1
                    self.__visited[copy_coords.y][copy_coords.x] = True
                copy_coords += direction

    def finish_exploring(self):
        return self.__how_many_visited

    def __precompute_available_directions_for_each_cell(self):
        self.__available_directions = [[None for x in range(self.m)] for y in range(self.n)]
        for x in range(self.n):
            for y in range(self.m):
                self.__precompute_directions(Coords(x, y))
                #print("x: ", x, " y: ", y, " direction: ", self.__available_directions[y][x])
        #print("breakpoint")

    def __precompute_directions(self, coords: Coords):
        self.__available_directions[coords.y][coords.x] = list()

        if self.surface[coords.y][coords.x] == 1:
            return

        for direction in range(len(DIRECTIONS)):
            next_coords = coords + DIRECTIONS[direction]
            if self.is_valid_cell(next_coords):
                self.__available_directions[coords.y][coords.x].append(direction)
