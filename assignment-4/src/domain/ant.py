from random import randint
from src.utils.config import *
from src.utils.variables import *
from src.domain.map import Map
import random



class Ant(object):
    def __init__(self, map: Map, first_coords: Coords):
        self.path = [first_coords]
        self.__map = map
        self.__how_much_stayed_at_sensor = 0
        self.__visited_sensors = dict()
        self.fitness = 0.1

    def find_available_directions(self, prev_coords):
        if self.__map.get_cell_value(Coords(prev_coords.x, prev_coords.y)) == 2 and (prev_coords.x, prev_coords.y) not in self.__visited_sensors and self.__how_much_stayed_at_sensor < 5 and self.__map.get_sensors()[(prev_coords.x, prev_coords.y)][self.__how_much_stayed_at_sensor] != 0:
            if self.__how_much_stayed_at_sensor == 4:
                self.__visited_sensors[(prev_coords.x, prev_coords.y)] = True
            self.__how_much_stayed_at_sensor += 1
            return [Coords(0, 0)]
        return self.__map.get_available_directions_for_cell(prev_coords)

    def __was_sensor_visited(self, sensor):
        return (sensor.x, sensor.y) in self.__visited_sensors

    def heuristic_for_distance(self, pos_x, pos_y, final_x, final_y):
        return abs(pos_x - final_x) + abs(pos_y - final_y)

    def compute_heuristic(self, coords) -> int:
        max_heuristic_ratio = 0
        for sensor_coords in self.__map.get_sensors():
            heuristic_for_counters = sum(self.__map.get_sensors()[sensor_coords]) * 1.2
            heuristic_for_distance = self.heuristic_for_distance(coords.x, coords.y, sensor_coords[0], sensor_coords[1])
            if (sensor_coords[0], sensor_coords[1]) in self.__visited_sensors:
                continue
            if heuristic_for_distance != 0:
                heuristic_ratio = heuristic_for_counters / heuristic_for_distance
            else:
                heuristic_ratio = heuristic_for_counters

            max_heuristic_ratio = max(max_heuristic_ratio, heuristic_ratio)
        return max_heuristic_ratio

    def choose_coords_to_proceed(self, prev_coords: Coords, available_directions):
        sensors = self.__map.get_sensors()
        if len(sensors) == len(self.__visited_sensors):
            return []

        maxx = [Coords(-1, -1), -1]
        p_vector = []
        for dir in available_directions:
            next_coords = prev_coords + dir
            h = self.compute_heuristic(next_coords)
            trace = self.__map.trace[next_coords.y][next_coords.x]
            p = (h ** BETA) * (trace ** ALPHA)
            p_vector.append([next_coords, p])
            if p > maxx[1]:
                maxx = [next_coords, p]

        if random.uniform(0, 1) < Q0:
            return maxx[0]
        else:
            sum_p = 0
            for p in p_vector:
                sum_p += p[1]

            if sum_p == 0:
                return random.choice(p_vector)

            for i in range(len(p_vector)):
                p_vector[i][1] = p_vector[i][1] / sum_p
            for i in range(len(p_vector)):
                summ = 0
                for j in range(0, i + 1):
                    summ += p_vector[j][1]
                p_vector[i][1] = summ

            r = random.uniform(0, 1)
            i = 0
            while r > p_vector[i][1]:
                i = i + 1
            return p_vector[i][0]

    def add_move(self):
        prev_coords = self.path[len(self.path) - 1]
        available_directions = self.find_available_directions(prev_coords)
        if available_directions[0] == Coords(0, 0):
            self.path.append(prev_coords)
            current_sensor_fitness = self.__map.get_sensors()[(prev_coords.x, prev_coords.y)][self.__how_much_stayed_at_sensor - 1]
            self.fitness += current_sensor_fitness
            return

        self.__how_much_stayed_at_sensor = -1
        next_coords = self.choose_coords_to_proceed(prev_coords, available_directions)
        self.path.append(next_coords)

    def get_fitness(self):
        return self.fitness

