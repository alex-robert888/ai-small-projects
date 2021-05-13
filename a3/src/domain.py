# -*- coding: utf-8 -*-

from random import *
from src.utils import *
import numpy as np
import pickle
import random


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation
class Gene(object):
    def __init__(self):
        self.value = -1

    def random(self, previous_cell):
        self.value = random.randint(0, len(DIRECTIONS) - 1)
        return self.value


class Individual:
    def __init__(self, size = 0, mapp = None):
        self.__size = size
        self.__chromosome = [Gene() for i in range(self.__size)]
        self.f = None
        self.__mapp = mapp
        self.__generate_chromosome()

    def __generate_chromosome(self):
        previous_cell = self.__mapp.starting_coords
        for gene_index in range(self.__size):
            direction = self.__chromosome[gene_index].random(previous_cell)
            previous_cell += DIRECTIONS[direction]

    def fitness(self):
        current_cell = self.__mapp.starting_coords
        self.__mapp.init_exploring()
        self.__mapp.explore(current_cell)
        for gene in self.__chromosome:
            current_cell += DIRECTIONS[gene]
        self.f = self.__mapp.finish_exploring()
        return self.f

    def mutate(self, mutateProbability = 0.2):
        if random() < mutateProbability:
            pass
            # perform a mutation with respect to the representation

    def crossover(self, otherParent, crossoverProbability = 0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size) 
        if random() < crossoverProbability:
            pass
            # perform the crossover between the self and the otherParent 
        
        return offspring1, offspring2
    
class Population():
    def __init__(self, population_size = 0, individual_size = 0, mapp = None):
        self.__populationSize = population_size
        self.__mapp = mapp
        self.__individuals = [Individual(individual_size, mapp) for x in range(population_size)]

    def evaluate(self):
        # evaluates the population
        for x in self.__individuals:
            x.fitness()
            
            
    def selection(self, k = 0):
        # perform a selection of k individuals from the population
        # and returns that selection
        self.evaluate()


        for x in self.__individuals:
            if

class Map(object):
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
        self.available_directions = []
        self.starting_coords = Coords(-1, -1)
        self.visited = []
        self.how_many_visited = 0

    def init_exploring(self):
        self.visited = [[False] * self.m] * self.n
        self.how_many_visited = 0

    def explore(self, coords):
        for direction in DIRECTIONS:
            while self.__is_valid_cell(coords):
                coords += direction
                if not self.visited[coords.i][coords.j]:
                    self.how_many_visited += 1
                    self.visited[coords.i][coords.j] = True

    def finish_exploring(self):
        return self.how_many_visited

    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1

    def __is_valid_cell(self, coords: Coords):
        return 0 <= coords.i < self.n and 0 <= coords.j < self.m and self.surface[coords.i, coords.j] == 0

    def __precompute_directions(self, coords: Coords):
        self.available_directions[coords.i][coords.j] = list()
        for direction in range(len(DIRECTIONS)):
            if self.__is_valid_cell(coords + DIRECTIONS[direction]):
                self.available_directions[coords.i][coords.j].append(direction)

    def __precompute_available_directions_for_each_cell(self):
        self.available_directions = [[[]]*self.m]*self.n
        for i in range(self.n):
            for j in range(self.m):
                self.__precompute_directions(Coords(i, j))

    def load_map(self, map_file_path, starting_coords) -> None:
        with open(map_file_path, "rb") as f:
            loaded_map = pickle.load(f)
            self.n = loaded_map.n
            self.m = loaded_map.m
            self.surface = loaded_map.surface
            self.starting_coords = starting_coords
            self.__precompute_available_directions_for_each_cell()

    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    