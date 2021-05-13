import pickle
import numpy
import pygame
import time

from src.drone_controller import DroneController
from src.model.coords import Coords
from src.model.map import Map

CELL_SIZE = 20
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)

class MapView(object):
    def __init__(self, map_file_path: str):
        self.__mapp = Map(map_file_path)
        self.__initial_coords = Coords(1, 5)
        self.__final_coords = Coords(19, 15)
        self.__drone_controller = DroneController(initial_coords=self.__initial_coords, final_coords=self.__final_coords,
                                                  mapp=self.__mapp)
        self.__running = False
        self.__cell = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.__cell.fill(BLUE)
        self.__surface = None
        self.__screen = None

        self.init_pygame()

    def render(self) -> None:
        self.__running = True
        self.__run_drone()

    def init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption("Path in simple environment")
        self.__screen = pygame.display.set_mode((CELL_SIZE * self.__mapp.n, CELL_SIZE * self.__mapp.m))
        self.__screen.fill(WHITE)

    def __render_map(self) -> None:
        self.__surface = pygame.Surface((CELL_SIZE * self.__mapp.n, CELL_SIZE * self.__mapp.m))
        self.__surface.fill(WHITE)

        for x in range(self.__mapp.n):
            for y in range(self.__mapp.m):
                if self.__mapp.get_cell(x, y) == 1:
                    self.__surface.blit(self.__cell, (y * CELL_SIZE, x * CELL_SIZE))

    def __mark_final_and_initial_cells(self):
        self.__cell.fill(GREEN)
        self.__surface.blit(self.__cell, (self.__initial_coords.x * CELL_SIZE, self.__initial_coords.y * CELL_SIZE))
        self.__surface.blit(self.__cell, (self.__final_coords.x * CELL_SIZE, self.__final_coords.y * CELL_SIZE))

    def __run_drone(self):

        t0 = time.time()
        path = self.__drone_controller.search_greedy()
        t1 = time.time()
        print("Path length: ", len(path))
        print("Path: ", path)

        self.__render_map()

        self.__mark_final_and_initial_cells()

        self.__cell.fill(PURPLE)
        index = 1
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

            if index < len(path) - 1:
                new_cell = path[index]
                self.__surface.blit(self.__cell, (new_cell[0] * CELL_SIZE, new_cell[1] * CELL_SIZE))
                index += 1
                time.sleep(0.15)

            self.__screen.blit(self.__surface, (0, 0))
            pygame.display.flip()
        pygame.quit()
