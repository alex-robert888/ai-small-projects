from src.view.gui import Gui


class Ui(object):
    def __init__(self):
        self.__is_running = False
        self.__gui: Gui = None

    def do_before_running_gui(self):
        pass

    def run(self):
        self.do_before_running_gui()
        while self.__is_running:
            self.__gui.render()

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