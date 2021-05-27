import numpy
import pickle
from enum import Enum
from src.domain.coords import Coords
from src.utils.variables import *
from src.utils.config import *
from queue import PriorityQueue


class MapCell(Enum):
    EMPTY = 1
    OBSTACLE = 2


def h(pos_x, pos_y, final_x, final_y):
    return abs(pos_x - final_x) + abs(pos_y - final_y)


def g(pos_x, pos_y, initial_x, initial_y):
    return abs(pos_x - initial_x) + abs(pos_y - initial_y)


class Map(object):
    def __init__(self):
        self.n = 0
        self.m = 0
        self.surface: numpy.matrix = None
        self.__starting_coords = Coords(STARTING_COORDS_X, STARTING_COORDS_Y)
        self.__available_directions = []
        self.__visited = []
        self.__how_many_visited = 0
        self.__sensors = dict()
        self.__min_paths_each_pair = dict()
        self.trace = []

    def get_cell_value(self, coords):
        if 0 <= coords.x <= self.n and 0 <= coords.y <= self.m:
            return self.surface[coords.y][coords.x]

    def get_starting_coords(self):
        return self.__starting_coords

    def get_available_directions_for_cell(self, coords: Coords):
        available_directions_indices = self.__available_directions[coords.y][coords.x]
        av_dirs = []
        for index in available_directions_indices:
            av_dirs.append(DIRECTIONS[index])
        return av_dirs

    def is_valid_cell(self, coords: Coords):
        return 0 <= coords.x < self.n and 0 <= coords.y < self.m and self.surface[coords.y, coords.x] == 0

    def print_surface(self):
        print("---- surface")
        for x in range(self.n):
            for y in range(self.m):
                print(self.surface[y][x], end=' ')
            print()
        print("------------")

    def load_from_binary_file(self, map_file_path: str):
        with open(map_file_path, "rb") as f:
            loaded_map = pickle.load(f)
            self.n = loaded_map.n
            self.m = loaded_map.m
            self.surface = loaded_map.surface
            self.trace = [[1 for i in range(self.n)] for j in range(self.m)]
            self.__precompute_available_directions_for_each_cell()
            self.populate_sensors()
            self.print_surface()

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

    def __precompute_directions(self, coords: Coords):
        self.__available_directions[coords.y][coords.x] = list()

        if self.surface[coords.y][coords.x] == 1:
            return

        for direction in range(len(DIRECTIONS)):
            next_coords = coords + DIRECTIONS[direction]
            if self.is_valid_cell(next_coords):
                self.__available_directions[coords.y][coords.x].append(direction)

    # region - SENSORS
    def populate_sensors(self):
        self.__sensors[(10, 5)] = []
        self.__sensors[(7, 8)] = []
        self.__sensors[(10, 7)] = []
        self.__sensors[(6, 3)] = []
        self.__sensors[(9, 11)] = []
        self.__sensors[(4, 4)] = []
        self.__sensors[(12, 5)] = []

        for sensor in self.__sensors:
            self.surface[sensor[1], sensor[0]] = 2

        self.cells_detected()
        # self.min_distance_between_each_pair()
        print("---- Sensors: ", self.__sensors)
        print("---- Min paths for each pair ", self.__min_paths_each_pair)

    def cells_detected(self):
        for sensor_coords in self.__sensors:
            dirs = list()
            dirs.append(Coords(sensor_coords[0], sensor_coords[1]))
            dirs.append(Coords(sensor_coords[0], sensor_coords[1]))
            dirs.append(Coords(sensor_coords[0], sensor_coords[1]))
            dirs.append(Coords(sensor_coords[0], sensor_coords[1]))
            for i in range(5):
                counter = self.go_one_step_in_all_directions(dirs)
                self.__sensors[sensor_coords].append(counter)

    def go_one_step_in_all_directions(self, dirs):
        counter = 0
        for i in range(len(DIRECTIONS)):
            next_cell = dirs[i] + DIRECTIONS[i]
            if self.is_valid_cell(next_cell):
                dirs[i] = next_cell
                counter += 1
        return counter

    def a_star(self, initial_coords: Coords, final_coords: Coords):
        priority_queue = PriorityQueue()
        priority_queue.put((h(initial_coords.x, initial_coords.y, final_coords.x, final_coords.y), Coords(initial_coords.x, initial_coords.y)))

        was_visited = numpy.zeros((20, 20))
        prev_matrix = numpy.zeros((20, 20), dtype=Coords)
        while not priority_queue.empty():
            current_coords = priority_queue.get()[1]
            was_visited[current_coords.y, current_coords.x] = True
            if current_coords.x == final_coords.x and current_coords.y == final_coords.y:
                return self.__reconstruct_path(initial_coords, final_coords, prev_matrix)
            for direction in DIRECTIONS:
                next_step = current_coords + direction
                if self.is_valid_cell(next_step) and not was_visited[next_step.y][next_step.x]:
                    prev_matrix[next_step.y, next_step.x] = Coords(current_coords.x, current_coords.y)
                    priority_queue.put((h(next_step.x, next_step.y, final_coords.x, final_coords.y) + g(next_step.x, next_step.y, initial_coords.x, initial_coords.y), Coords(next_step.x, next_step.y)))
        return []

    @staticmethod
    def __reconstruct_path(initial_coords: Coords, final_coords: Coords, prev_matrix):
        path = []
        current_coords = final_coords
        while True:
            path.append((current_coords.x, current_coords.y))
            if current_coords.x == initial_coords.x and current_coords.y == initial_coords.y:
                break
            prev = prev_matrix[current_coords.y, current_coords.x]
            current_coords = prev
        return path

    def get_sensors(self):
        return self.__sensors