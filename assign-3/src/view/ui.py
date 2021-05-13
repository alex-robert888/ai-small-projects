from src.view.gui import Gui
from src.domain.map import Map
from src.controller.controller import Controller
from src.utils.config import *


class Ui(object):
    def __init__(self):
        self.__is_running = False
        self.__is_running_gui = False
        self.__map = Map()
        self.__gui: Gui = Gui(self.__map)
        self.__controller: Controller = None

    def do_before_running_gui(self):
        self.__gui.initialize()

    def visualize_map(self):
        self.do_before_running_gui()
        self.__is_running_gui = True
        while self.__is_running_gui:
            self.__is_running_gui = self.__gui.render()
        self.__gui.quit()

    def run(self):
        self.__is_running = True
        while self.__is_running:
            self.__print_menu()
            option = int(input(" >> "))
            if option == 0:
                self.__map.load_from_binary_file("../assets/test1.map")
                self.visualize_map()
            if option == 1:
                self.__map.load_from_binary_file("../assets/test1.map")
                self.__controller = Controller(self.__map)
                self.__controller.run()
            elif option == 2:
                self.do_before_running_gui()
                fittest_individual = self.__controller.fittest_individual
                gene_index = 0
                self.__is_running_gui = True
                while self.__is_running_gui:
                    if gene_index < INDIVIDUAL_SIZE:
                        self.__is_running_gui = self.__gui.render(gene_index, fittest_individual)
                        gene_index += 1
                self.__gui.quit()
            elif option == 3:
                pass
            elif option == 4:
                self.visualize_map()

    @staticmethod
    def __print_menu():
        # print(
        #       "1. map options:\n"
        #       "      a. create random map\n"
        #       "      b. load a map\n"
        #       "      c. save a map\n"
        #       "      d visualise map\n"
        #       "2. EA options:\n"
        #       "      a. parameters setup\n"
        #       "      b. run the solver\n"
        #       "      c. visualise the statistics\n"
        #       "      d. view the drone moving on a path\n"
        # )
        print(
            "0. load map\n"
            "1. run EA\n"
            "2. visualize solution\n",
            "3. view statistics\n"
            "4. view map\n"
        )
