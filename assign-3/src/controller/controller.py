from src.repository.repository import Repository
from src.utils.config import *
from src.domain.individual import Individual

class Controller(object):
    def __init__(self, mapp):
        self.__repository = Repository(mapp)
        self.__population_size = POPULATION_SIZE
        self.__individual_size = INDIVIDUAL_SIZE
        self.__map = mapp
        self.fittest_individual = None

    def prepare_algorithm(self):
        self.__repository.initialize_population(self.__population_size, self.__individual_size)

    def iteration(self):
        # args - list of parameters needed to run one iteration
        # an iteration:
        # selection of the parents
        population = self.__repository.get_active_population()
        selected_parents = population.apply_tournaments_selection(NUMBER_OF_INDIVIDUALS_FOR_PARENTS_SELECTION)

        # create offsprings by crossover and mutate them
        offsprings = []
        for i in range(len(selected_parents) - 1):
            for j in range(i + 1, len(selected_parents)):
                new_offsprings = selected_parents[i].crossover(selected_parents[j])
                if new_offsprings is None:
                    continue
                offsprings.append(new_offsprings[0].mutate())
                offsprings.append(new_offsprings[1].mutate())

        # selection of the survivors
        next_generation_individuals = population.apply_tournaments_selection(POPULATION_SIZE - len(offsprings))
        next_generation_individuals.extend(offsprings)
        population.refresh_individuals(next_generation_individuals)

    def run(self):
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        self.fittest_individual: Individual = None
        for run in range(NUMBER_OF_RUNS):
            self.prepare_algorithm()
            print("Run no. ", run)
            for i in range(NUMBER_OF_ITERATIONS):
                self.iteration()

            if self.fittest_individual is None:
                self.fittest_individual = self.__repository.get_active_population().get_fittest_candidate()
            elif self.fittest_individual.get_fitness() < self.__repository.get_active_population().get_fittest_candidate().get_fitness():
                self.fittest_individual = self.__repository.get_active_population().get_fittest_candidate()

            print("Max Fitness: ", self.fittest_individual.get_fitness())


