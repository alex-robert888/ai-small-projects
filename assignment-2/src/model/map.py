import pickle
import numpy


class Map(object):
    def __init__(self, map_file_path: str):
        self.map_file_path = map_file_path
        self.n = 0
        self.m = 0
        self.__surface: numpy.matrix = None

        self.__load_map_config()

    def valid_position(self, x, y):
        return 0 <= x <= 19 and 0 <= y <= 19 and self.__surface[y, x] != 1

    def __load_map_config(self) -> None:
        with open(self.map_file_path, "rb") as f:
            loaded_map = pickle.load(f)
            self.n = loaded_map.n
            self.m = loaded_map.m
            self.__surface = loaded_map.surface

    def get_cell(self, x, y):
        return self.__surface[y, x]
