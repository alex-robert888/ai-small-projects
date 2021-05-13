# -*- coding: utf-8 -*-


# imports
from src.gui import *
from src.controller import *
from src.repository import *
from src.domain import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls


class Ui(object):
    def __init__(self):
        self.__map = Map()
        self.__map.load_map("assets/test1.map", Coords(5, 1))
        self.__controller = Controller(self.__map)
        self.__running = False

    @staticmethod
    def __print_menu():
        print(
              "1. map options:\n"
              "      a. create random map\n"
              "      b. load a map\n"
              "      c. save a map\n"
              "      d visualise map\n"
              "2. EA options:\n"
              "      a. parameters setup\n"
              "      b. run the solver\n"
              "      c. visualise the statistics\n"
              "      d. view the drone moving on a path\n"
        )

    def __execute_command(self, first_option: int, second_option: str):
        if first_option == 1:
            if second_option == "a":
                self.__map.randomMap()
            elif second_option == "b":
                pass
            elif second_option == "c":
                pass
            elif second_option == "d":
                self.__screen = initPyGame((400, 400))
                self.__controller.prepare_algorithm()

                while self.__running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.__running = False
                    self.__screen.blit(image(self.__map), (0, 0))
                    pygame.display.flip()

        elif first_option == 2:
            if second_option == "a":
                pass
            elif second_option == "b":
                pass
            elif second_option == "c":
                pass
            elif second_option == "d":
                pass

    def run(self):
        self.__print_menu()
        self.__running = True
        self.__execute_command(1, "d")
        while self.__running:
            first_option = int(input("First option: "))
            if first_option != 1 and first_option != 2:
                print("Invalid option! You should choose an integer between 1 and 2")
                continue

            second_option = input("Second option: ")
            if second_option != "a" and second_option != "b" and second_option != "c" and second_option != "d":
                print("Invalid option! You should rchoose a character between a and d")
                continue
            self.__execute_command(first_option, second_option)
