from src.view.gui import Gui
from src.domain.map import Map
from src.controller.controller import Controller
import time


class Console(object):
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
            if option == 1:
                self.__controller = Controller(self.__map)
                self.best_solution = self.__controller.run()
                print("--------------- BEST SOLUTION -------------------- \n")
                print("--- Best Solution fitness: ", self.best_solution[0])
                print("--- Best Solution path: ", end=" ")
                for s in self.best_solution[1]:
                    print("(", s.x, ", ", s.y, ") ", end=" ")
            elif option == 2:
                self.do_before_running_gui()
                self.__is_running_gui = True
                time.sleep(1)
                index = 0
                while self.__is_running_gui:
                    self.__is_running_gui = self.__gui.render(self.best_solution, index)
                    index += 1
                    time.sleep(0.2)
                self.__gui.quit()
            elif option == 3:
                pass
            elif option == 4:
                self.visualize_map()

    @staticmethod
    def __print_menu():
        print(
            "0. load map\n"
            "1. run EA\n"
            "2. visualize solution\n",
            "3. view statistics\n"
            "4. view map\n"
        )