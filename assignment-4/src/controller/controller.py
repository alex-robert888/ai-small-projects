from src.utils.config import *
from src.domain.map import Map
from src.domain.ant import Ant
from src.domain.coords import Coords

import time


class Controller(object):
    def __init__(self, mapp):
        self.__map: Map = mapp
        self.__best_sol = []

    def __initialize_ant_colony(self):
        return [Ant(self.__map, Coords(STARTING_COORDS_X, STARTING_COORDS_Y)) for i in range(NUMBER_OF_ANTS)]

    def __add_one_step_to_each_ant(self, ants):
        for ant in ants:
            ant.add_move()

    def __update_pheromone_traces(self, ant_colony):
        d_trace = [1.0 / ant_colony[i].get_fitness() for i in range(len(ant_colony))]
        for x in range(self.__map.n):
            for y in range(self.__map.m):
                self.__map.trace[y][x] = (1 - RHO) * self.__map.trace[y][x]

        for i in range(len(ant_colony)):
            for coords in ant_colony[i].path:
                self.__map.trace[coords.y][coords.x] = self.__map.trace[coords.y][coords.x] + d_trace[i]

    def __best_solution(self, ant_colony):
        f = [[ant_colony[i].get_fitness(), ant_colony[i].path] for i in range(len(ant_colony))]
        f = max(f)
        return f

    def __run_epoch(self):
        ant_colony = self.__initialize_ant_colony()
        for unit in range(BATTERY_CAPACITY - 1):
            self.__add_one_step_to_each_ant(ant_colony)
        self.__update_pheromone_traces(ant_colony)
        return self.__best_solution(ant_colony)

    def best_of(self, solution_a, solution_b):
        return solution_a if solution_a[0] > solution_b[0] else solution_b

    def run(self):
        best_solution = [-1, []]
        for epoch in range(NUMBER_OF_EPOCHS):
            print("Epoch no. ", epoch)
            new_solution = self.__run_epoch()
            print("--- Solution fitness: ", new_solution[0])
            print("--- Solution path: ", end=" ")
            for s in new_solution[1]:
                print("(", s.x, ", ", s.y, ") ", end=" ")

            best_solution = self.best_of(best_solution, new_solution)

        return best_solution

