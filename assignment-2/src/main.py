from view.map_view import MapView
from model.map import Map
from model.drone import Drone


def main():
    map_view = MapView('../assets/maps/test1.map')
    map_view.render()


if __name__ == '__main__':
    main()
