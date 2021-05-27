import pygame
from src.domain.map import Map, MapCell
from src.domain.coords import Coords
from src.utils.config import *


class Gui(object):
    def __init__(self, mapp: Map):
        self.__LOGO_PATH = "../assets/logo32x32.png"
        self.__SCREEN_CAPTION = "Environment Exploration with EA"
        self.__CELL_SIZE = 30
        self.__BACKGROUND_COLOR = (235, 235, 235)
        self.__BRICK_COLOR = (22, 17, 43)
        self.__SENSOR_COLOR = (107, 173, 255)
        self.__STARTING_BRICK_COLOR = (0, 229, 145)

        self.__screen = None
        self.__map: Map = mapp

    def render(self, best_solution=None, best_solution_current_index=-1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.__screen.blit(self.__draw_map(best_solution, best_solution_current_index), (0, 0))
        pygame.display.flip()
        return True

    def quit(self):
        pygame.quit()

    def initialize(self):
        pygame.init()
        logo = pygame.image.load(self.__LOGO_PATH)
        pygame.display.set_icon(logo)
        pygame.display.set_caption(self.__SCREEN_CAPTION)
        self.__screen = pygame.display.set_mode((self.__map.n * self.__CELL_SIZE, self.__map.m * self.__CELL_SIZE))

    def __draw_map(self, best_solution=None, best_solution_current_index=-1):
        # Probably move this from here to not repeat this block every time
        map_surface = pygame.Surface((self.__map.n * self.__CELL_SIZE, self.__map.m * self.__CELL_SIZE))
        map_surface.fill(self.__BACKGROUND_COLOR)
        brick = pygame.Surface((self.__CELL_SIZE, self.__CELL_SIZE))

        brick.fill(self.__STARTING_BRICK_COLOR)
        map_surface.blit(brick, (self.__map.get_starting_coords().y * self.__CELL_SIZE, self.__map.get_starting_coords().x * self.__CELL_SIZE))

        brick.fill(self.__BRICK_COLOR)
        for x in range(self.__map.n):
            for y in range(self.__map.m):
                if self.__map.get_cell_value(Coords(x, y)) == 1:
                    brick.fill(self.__BRICK_COLOR)
                    map_surface.blit(brick, (y * self.__CELL_SIZE, x * self.__CELL_SIZE))
                elif self.__map.get_cell_value(Coords(x, y)) == 2:
                    brick.fill(self.__SENSOR_COLOR)
                    map_surface.blit(brick, (y * self.__CELL_SIZE, x * self.__CELL_SIZE))

        # Render best path
        if best_solution is not None:
            limit_index = min(best_solution_current_index + 1, BATTERY_CAPACITY)
            brick.fill(self.__STARTING_BRICK_COLOR)
            for i in range(0, limit_index):
                current_coords = best_solution[1][i]
                if self.__map.get_cell_value(Coords(x, y)) == 2:
                    continue
                map_surface.blit(brick, (current_coords.y * self.__CELL_SIZE, current_coords.x * self.__CELL_SIZE))

            current_coords = best_solution[1][limit_index - 1]
            drone = pygame.image.load("../assets/drona.png")
            map_surface.blit(drone, (current_coords.y * self.__CELL_SIZE, current_coords.x * self.__CELL_SIZE))
        else:
            drone = pygame.image.load("../assets/drona.png")
            map_surface.blit(drone, (STARTING_COORDS_Y * self.__CELL_SIZE, STARTING_COORDS_X * self.__CELL_SIZE))

        return map_surface
