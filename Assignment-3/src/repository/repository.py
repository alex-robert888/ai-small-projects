import pickle
from src.domain.population import Population


class Repository(object):
    def __init__(self, mapp):
        self.__populations = []
        self.__active_population_index = -1
        self.__map = mapp

    def initialize_population(self, population_size, individual_size):
        population = Population(population_size, individual_size, self.__map)
        self.__populations.append(population)
        self.__active_population_index = len(self.__populations) - 1
        return population

    def get_active_population(self) -> Population:
        return self.__populations[self.__active_population_index]

