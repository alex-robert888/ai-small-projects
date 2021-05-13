# -*- coding: utf-8 -*-

import pickle
from src.domain import *


class Repository(object):
    def __init__(self, mapp):
        self.__populations = []
        self.active_population_index = -1
        self.mapp = mapp
        
    def initialize_population(self, population_size, individual_size):
        population = Population(population_size, individual_size, self.mapp)
        self.__populations.append(population)
        self.active_population_index = len(self.__populations) - 1
        return population

    def get_active_population(self):
        return self.__populations[self.active_population_index]
