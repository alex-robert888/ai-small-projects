import pygame
from src.domain.map import Map


class Gui(object):
    def __init__(self):
        self.__LOGO_PATH = "assets/logo32x32.png"
        self.__SCREEN_CAPTION = "Environment Exploration with Evolutionary Algorithm"
        self.__CELL_SIZE = 20
        self.__BACKGROUND_COLOR = (22, 17, 43)
        self.__BRICK_COLOR = (235, 235, 235)

        self.__screen = None
        self.__map: Map = None
        self.__initialize_pygame()

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.__screen.blit(self.__draw_map(), (0, 0))
        pygame.display.flip()
        return True

    def quit(self):
        pygame.quit()

    def __initialize_pygame(self):
        pygame.init()
        logo = pygame.image.load(self.__LOGO_PATH)
        pygame.display.set_icon(logo)
        pygame.display.set_caption(self.__SCREEN_CAPTION)

    def __draw_map(self):
        # Probably move this from here to not repeat this block every time
        map_surface = pygame.Surface((self.__map.n * self.__CELL_SIZE, self.__map.m * self.__CELL_SIZE))
        brick = pygame.Surface((self.__CELL_SIZE, self.__CELL_SIZE))
        brick.fill(self.__BRICK_COLOR)
        map_surface.fill(self.__BACKGROUND_COLOR)

        for i in range(self.__map.n):
            for j in range(self.__map.m):
                if self.__map.get_cell_value(i, j) == Map:
                    map_surface.blit(brick, (j * self.__CELL_SIZE, i * self.__CELL_SIZE))
        return map_surface
