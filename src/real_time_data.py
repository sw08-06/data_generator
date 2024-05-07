import os
import time
import random
import numpy as np
import h5py
import influxdb_client


class DataGenerator:
    def __init__(self, file_path, amount_windows, stress_ratio, window_size, first_window_id):
        self.file_path = file_path
        self.window_size = window_size
        self.window_id = first_window_id
        self.amount_windows = amount_windows
        self.stress_ratio = stress_ratio
        self.subject_data = []

    def load_subject_data(self):
        with h5py.File(self.file_path, "r") as file:
            dataset_names = list(file.keys())
            random.shuffle(dataset_names)

            stress_cnt = np.floor(self.amount_windows * self.stress_ratio)
            no_stress_cnt = self.amount_windows - stress_cnt

            for dataset_name in dataset_names:
                dataset = file[dataset_name][:].flatten()
                if file[dataset_name].attrs["label"] == 0 and no_stress_cnt > 0:
                    self.subject_data.append(dataset)
                    no_stress_cnt -= 1
                elif file[dataset_name].attrs["label"] == 1 and stress_cnt > 0:
                    self.subject_data.append(dataset)
                    stress_cnt -= 1
        print(f"Loaded {self.amount_windows} datasets from {self.file_path} for data generation")

    def generate_window_data_points(self):
        """
        Generates one window of data points.
        Args:
            window_size (int): Size of window in seconds.
        Returns:
            list: List of data points.
        """
        data_dict = {"bvp": 64, "eda": 4, "temp": 4}
        data_points = []
        index = 0

        if len(self.subject_data) > 0:
            dataset = self.subject_data.pop(0)
        else:
            print("No more data")
            return

        for data_type in list(data_dict.keys()):
            sampling_step = int(np.round(1000000000 / data_dict[data_type]))
            for i in range(self.window_size * data_dict[data_type]):
                data_point_value = dataset[index + i]
                print(time.time_ns() + sampling_step * i)
                data_points.append(
                    influxdb_client.Point("data")
                    .time(time.time_ns() + sampling_step * i)
                    .tag("data_type", data_type)
                    .field("window_id", self.window_id)
                    .field("index", index + i)
                    .field("value", data_point_value)
                )
            index += self.window_size * data_dict[data_type]
        print(f"Generated window data points with window_id: {self.window_id}")
        self.window_id += 1
        return data_points


if __name__ == "__main__":
    dataGenerator = DataGenerator(file_path=os.path.join("data", "testing.h5"), amount_windows=100, stress_ratio=0.5, window_size=60, first_window_id=100000)
    dataGenerator.load_subject_data()
    data_points = dataGenerator.generate_window_data_points()
