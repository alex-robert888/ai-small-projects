from src.utils.variables import *
from src.utils.config import *
from src.domain.gene import Gene
from src.domain.map import Map
import random


class Individual(object):
    def __init__(self, size=0, mapp=None):
        self.__size = size
        self.__chromosome = [Gene() for i in range(self.__size)]
        self.__f = None
        self.__map: Map = mapp
        self.__generate_chromosome()

    def __generate_chromosome(self):
        previous_cell = self.__map.get_starting_coords()
        if self.__map.get_cell_value(Coords(previous_cell.y, previous_cell.x)) == 1:
            print("OBSTACLE STARTING POINT")
            return

        for gene_index in range(self.__size):
            # print("previous cell: x: ", previous_cell.x,  ", y: ", previous_cell.y, "  directions: ", self.__map.get_available_directions_for_cell(previous_cell))
            previous_cell = self.__chromosome[gene_index].random(previous_cell, self.__map.get_available_directions_for_cell(previous_cell))
            if self.__map.get_cell_value(Coords(previous_cell.x, previous_cell.y)) == 1:
                print("============ OBSTACLE ===============")
                return

    def recalculate_fitness(self):
        current_cell = self.__map.get_starting_coords()
        self.__map.init_exploring()

        self.__map.explore(current_cell)
        for gene in self.__chromosome:
            self.__map.explore(gene.coords)

        self.__f = self.__map.finish_exploring()
        #print("Finish Exploring", self.__f)
        return self.__f

    def get_fitness(self):
        return self.__f

    def get_gene(self, gene_index) -> Gene:
        return self.__chromosome[gene_index]

    def set_gene(self, index, value):
        self.__chromosome[index] = value

    def add_direction_to_gene(self, previous_gene, direction):
        next_gene = Gene()
        next_gene.coords = previous_gene.coords + DIRECTIONS[direction]
        next_gene.from_direction = direction
        if not self.__map.is_valid_cell(next_gene.coords):
            next_gene.random(previous_gene.coords, self.__map.get_available_directions_for_cell(previous_gene.coords))
        return next_gene

    def mutate(self, mutate_probability=0.2):
        if random.uniform(0, 1) < mutate_probability:
            previous_coords = self.__map.get_starting_coords()
            for gene_index in range(INDIVIDUAL_SIZE):
                if random.uniform(0, 1) < GENE_MUTATION_PROBABILITY:
                    self.__chromosome[gene_index].random(previous_coords, self.__map.get_available_directions_for_cell(previous_coords))
                previous_coords = self.__chromosome[gene_index].coords

        return self

    def crossover(self, other_parent, crossover_probability=0.8):
        if random.uniform(0, 1) < crossover_probability:
            offspring1, offspring2 = Individual(self.__size, self.__map), Individual(self.__size, self.__map)
            offspring1.set_gene(0, self.get_gene(0))
            offspring2.set_gene(0, other_parent.get_gene(0))

            for gene_index in range(1, INDIVIDUAL_SIZE):
                if gene_index % 2 == 0:
                    offspring1.set_gene(gene_index, offspring1.add_direction_to_gene(offspring1.get_gene(gene_index - 1), self.get_gene(gene_index).from_direction))
                    offspring2.set_gene(gene_index, offspring2.add_direction_to_gene(offspring2.get_gene(gene_index - 1), other_parent.get_gene(gene_index).from_direction))
                else:
                    offspring1.set_gene(gene_index, offspring1.add_direction_to_gene(offspring1.get_gene(gene_index - 1), other_parent.get_gene(gene_index).from_direction))
                    offspring2.set_gene(gene_index, offspring2.add_direction_to_gene(offspring2.get_gene(gene_index - 1), self.get_gene(gene_index).from_direction))

            return [offspring1, offspring2]
        return None
