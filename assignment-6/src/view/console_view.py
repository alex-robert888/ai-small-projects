from src.controller.console_controller import ConsoleController


class ConsoleView(object):
    def __init__(self):
        self.__is_running = False
        self.__console_controller = ConsoleController()

    def run(self):
        self.__is_running = True
        while self.__is_running:
            self.print_menu()
            try:
                option = int(input(">> "))
                if option == 1:
                    self.__console_controller.load_dataset()
                elif option == 2:
                    self.__console_controller.run_kmeans()
                else:
                    print("Invalid option! Please try again..")
            except Exception as exc:
                print("Something unexpected occur. Try entering an option again..")
                print(exc)

    def print_menu(self):
        print(
            "\n\n------- MAIN MENU -------\n"
            "1. Load data.\n"
            "2. Run k-means algorithm."
        )
