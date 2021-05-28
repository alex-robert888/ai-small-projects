from typing import final
import matplotlib.pyplot as plt
import random
import sys
import time

class DataLabel(object):
    # Expecting a value from [0, 1, 2, 3]
    def __init__(self, value: str=""):
        self.VALUES: final = ['A', 'B', 'C', 'D']
        self.value = value

    def set_from_index(self, index: int) -> None:
        self.value = self.VALUES[index]

    def from_value_to_index(self) -> int:
        return self.VALUES.index(self.value.upper())


class DataRecord(object):
    def __init__(self, label: DataLabel, value1: float, value2: float):
        self.label = label
        self.value1 = value1
        self.value2 = value2


class ConsoleController(object):
    def __init__(self):
        self.__dataset: list[DataRecord] = []
        self.__centroids: list[DataRecord] = []
        self.__DATASET_FILE_PATH: final = "data/dataset.csv"
        self.__NUMBER_OF_CENTROIDS: final = 4
        self.__ITERATIONS_UNTIL_CONVERGENCE = 20
        self.__iteration = 0
        self.__plot_data = []
        self.__PLOT_COLORS: final = ['#0eedc4', '#ff8a2b', '#ff2b6e', '#442bff']
        self.__was_convergence_reached: bool = False

    def load_dataset(self):
        self.__dataset = []
        dataset_file = open(self.__DATASET_FILE_PATH, 'r')
        records = dataset_file.readlines()
        for record in records[1:]:
            processed_record = record.rstrip('\n').split(',')
            label = DataLabel('')
            value1 = float(processed_record[1])
            value2 = float(processed_record[2])
            self.__dataset.append(DataRecord(label, value1, value2))
        print("Data successfully loaded.")

    def run_kmeans(self) -> str:
        self.__centroids = self.__select_centroids()

        while not self.__was_convergence_reached:
            self.__cluster_records()
            self.__centroids = self.__recompute_centroids()
            self.__print_centroids()

        self.__plot_clusters()
        return self.__compute_statistical_measures()

    def __print_centroids(self):
        print("------ Centroids ------")
        index = 1
        for centroid in self.__centroids:
            print("Centroid no.", index, centroid.label.value, centroid.value1, centroid.value2)
            index += 1
        print("")

    def __select_centroids(self) -> list[DataRecord]:
        centroids = random.sample(self.__dataset.copy(), self.__NUMBER_OF_CENTROIDS)
        centroids[0].label.value = "A"
        centroids[1].label.value = "B"
        centroids[2].label.value = "C"
        centroids[3].label.value = "D"
        return centroids

    def __cluster_records(self) -> None:
        for record in self.__dataset:
            record.label = self.__compute_arg_min(record)

    def __compute_arg_min(self, record) -> DataLabel:
        closest_centroid_index: int = -1
        closest_distance: float = sys.float_info.max
        for centroid_index in range(len(self.__centroids)):
            current_distance = self.__compute_squared_euclidean_distance(record, self.__centroids[centroid_index])
            if closest_distance > current_distance:
                closest_centroid_index = centroid_index
                closest_distance = current_distance
        return self.__centroids[closest_centroid_index].label

    @staticmethod
    def __compute_squared_euclidean_distance(record, centroid) -> float:
        return (record.value1 - centroid.value1) ** 2 + (record.value2 - centroid.value2) ** 2

    def __recompute_centroids(self) -> list[DataRecord]:
        new_centroids: list[DataRecord] = [
            DataRecord(label=DataLabel(label_value), value1=0, value2=0)
            for label_value in DataLabel().VALUES
        ]
        new_centroids_counters: list[int] = [0 for i in range(0, 4)]
        for record in self.__dataset:
            centroid_index = record.label.from_value_to_index()
            new_centroids[centroid_index].value1 += record.value1
            new_centroids[centroid_index].value2 += record.value2
            new_centroids_counters[centroid_index] += 1

        for centroid in new_centroids:
            centroid.value1 = centroid.value1 / new_centroids_counters[centroid.label.from_value_to_index()]
            centroid.value2 = centroid.value2 / new_centroids_counters[centroid.label.from_value_to_index()]

        self.check_if_convergence_was_reached(new_centroids)
        return new_centroids

    def check_if_convergence_was_reached(self, new_centroids):
        for i in range(len(new_centroids)):
            if new_centroids[i].value1 != self.__centroids[i].value1 or new_centroids[i].value2 != self.__centroids[i].value2:
                return
        self.__was_convergence_reached = True

    def __plot_clusters(self):
        print("Plotting in progress..")
        for record in self.__dataset:
            record_cluster_index: int = record.label.from_value_to_index()
            plt.scatter(record.value1, record.value2, c=self.__PLOT_COLORS[record_cluster_index])
        plt.show()

    def __compute_statistical_measures(self) -> str:
        pass
