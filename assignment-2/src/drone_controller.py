from src.model.drone import Drone
from src.model.map import Map
from src.model.coords import Coords
from queue import PriorityQueue
import numpy

class DroneController(object):
    def __init__(self, initial_coords: Coords, final_coords: Coords, mapp: Map):
        self.drone = Drone()
        self.mapp = mapp
        self.initial_coords = initial_coords
        self.final_coords = final_coords
        self.prev_matrix = numpy.zeros((20, 20), dtype=Coords)
        self.DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def search_greedy(self):
        priority_queue = PriorityQueue()
        priority_queue.put((self.h(self.initial_coords.x, self.initial_coords.y), Coords(self.initial_coords.x, self.initial_coords.y)))

        was_visited = numpy.zeros((20, 20))
        self.prev_matrix[self.initial_coords.y, self.initial_coords.x] = Coords(-1, -1)
        while not priority_queue.empty():
            current_coords = priority_queue.get()[1]
            was_visited[current_coords.y, current_coords.x] = True
            if current_coords.x == self.final_coords.x and current_coords.y == self.final_coords.y:
                return self.__reconstruct_path()
            for direction in self.DIRECTIONS:
                next_x = current_coords.x + direction[0]
                next_y = current_coords.y + direction[1]
                if self.mapp.valid_position(next_y, next_x) and not was_visited[next_y][next_x]:
                    self.prev_matrix[next_y, next_x] = Coords(current_coords.x, current_coords.y)
                    priority_queue.put((self.h(next_x, next_y), Coords(next_x, next_y)))
        return []

    def search_a_star(self):
        priority_queue = PriorityQueue()
        priority_queue.put((self.h(self.initial_coords.x, self.initial_coords.y), Coords(self.initial_coords.x, self.initial_coords.y)))

        was_visited = numpy.zeros((20, 20))
        self.prev_matrix[self.initial_coords.y, self.initial_coords.x] = Coords(-1, -1)
        while not priority_queue.empty():
            current_coords = priority_queue.get()[1]
            was_visited[current_coords.y, current_coords.x] = True
            if current_coords.x == self.final_coords.x and current_coords.y == self.final_coords.y:
                return self.__reconstruct_path()
            for direction in self.DIRECTIONS:
                next_x = current_coords.x + direction[0]
                next_y = current_coords.y + direction[1]
                if self.mapp.valid_position(next_y, next_x) and not was_visited[next_y][next_x]:
                    self.prev_matrix[next_y, next_x] = Coords(current_coords.x, current_coords.y)
                    priority_queue.put((self.h(next_x, next_y) + self.g(next_x, next_y), Coords(next_x, next_y)))
        return []

    def __reconstruct_path(self):
        path = []
        current_coords = self.final_coords
        while True:
            path.append((current_coords.x, current_coords.y))
            if current_coords.x == self.initial_coords.x and current_coords.y == self.initial_coords.y:
                break
            prev = self.prev_matrix[current_coords.y, current_coords.x]
            current_coords = prev
        return path

    def h(self, pos_x, pos_y):
        return abs(pos_x - self.final_coords.x) + abs(pos_y - self.final_coords.y)

    def g(self, pos_x, pos_y):
        return abs(pos_x - self.initial_coords.x) + abs(pos_y - self.initial_coords.y)

