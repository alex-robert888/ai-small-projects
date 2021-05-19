from src.domain.individual import Individual
from src.utils.config import *
import random


class Population(object):
    def __init__(self, population_size=5, individual_size=10, mapp=None):
        self.__populationSize = population_size
        self.__mapp = mapp
        self.__individuals = [Individual(individual_size, mapp) for _ in range(population_size)]

    def evaluate(self):
        for individual in self.__individuals:
            individual.recalculate_fitness()

    def refresh_individuals(self, individuals):
        self.__individuals = individuals

    def select_max_fitness_individual_from_sample(self, sample):
        max_fitness_index = 0
        for individual_index in sample:
            if self.__individuals[individual_index].get_fitness() > self.__individuals[max_fitness_index].get_fitness():
                max_fitness_index = individual_index
        return self.__individuals[max_fitness_index]

    def apply_tournaments_selection(self, number_of_candidates):
        self.evaluate()
        candidates = list()
        for i in range(number_of_candidates):
            random_sample = random.sample(range(0, len(self.__individuals)), SIZE_OF_TOURNAMENT)
            max_fitness_individual = self.select_max_fitness_individual_from_sample(random_sample)
            candidates.append(max_fitness_individual)
        return candidates

    def get_fittest_candidate(self) -> Individual:
        self.evaluate()

        fittest_individual = self.__individuals[0]
        for individual in self.__individuals:
            if individual.get_fitness() > fittest_individual.get_fitness():
                fittest_individual = individual
        return fittest_individual

    def get_average_fitness(self):
        self.evaluate()
        average = 0
        for individual in self.__individuals:
            average += individual.get_fitness()
        return average / len(self.__individuals)