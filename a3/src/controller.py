from src.repository import *


class Controller(object):
    def __init__(self, mapp):
        self.__repository = Repository(mapp)
        self.__population_size = 10
        self.__individual_size = 5
        self.mapp = mapp

    def prepare_algorithm(self):
        self.__repository.initialize_population(self.__population_size, self.__individual_size)

    def iteration(self):
        # args - list of parameters needed to run one iteration
        # an iteration:
        # selection of the parents
        population = self.__repository.get_active_population()

        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        pass
        
    def run(self):
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        for i in range(0, 1):
            self.iteration()

        # return the results and the info for statistics
        pass
    
    
    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        
        # create the population,

        # run the algorithm
        # return the results and the statistics
        pass
       