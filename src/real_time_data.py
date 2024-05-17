import time
import random
import numpy as np
import h5py
from sklearn.preprocessing import MinMaxScaler


class DataGenerator:
    def __init__(self, file_path, amount_windows, stress_ratio, window_size, first_window_id):
        """
        Initialize DataGenerator instance.

        Args:
            file_path (str): Path to the HDF5 file containing subject data.
            amount_windows (int): Total number of windows to generate.
            stress_ratio (float): Ratio of stress windows to total windows.
            window_size (int): Size of each window in seconds.
            first_window_id (int): ID to start assigning to windows.
        """
        self.file_path = file_path
        self.window_size = window_size
        self.window_id = first_window_id
        self.amount_windows = amount_windows
        self.stress_ratio = stress_ratio
        self.subject_data = []
        self.start_time = time.time_ns() - window_size * 10**9

    def load_subject_data(self):
        """
        Loads and shuffles subject data in the specified amount of windows from the HDF5 file.
        """
        print("Loading subject data...")
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
        Generates data points for a single window.

        Returns:
            list: List of InfluxDB data points.
        """
        print("Generating window data points...")
        data_dict = {"bvp": 64, "eda": 4, "temp": 4}
        data_points = []
        data_list = []
        index = 0

        if len(self.subject_data) > 0:
            dataset = self.subject_data.pop(0)

            data_list.append(dataset[0 : data_dict["bvp"] * self.window_size])
            data_list.append(dataset[data_dict["bvp"] * self.window_size : data_dict["bvp"] * self.window_size + data_dict["eda"] * self.window_size])
            data_list.append(
                dataset[
                    data_dict["bvp"] * self.window_size
                    + data_dict["eda"] * self.window_size : data_dict["bvp"] * self.window_size
                    + data_dict["eda"] * self.window_size
                    + data_dict["temp"] * self.window_size
                ]
            )

            for data in data_list:
                data = MinMaxScaler().fit_transform(data[:, np.newaxis])

            dataset = np.concatenate(data_list)[:].flatten()

        else:
            print("No more data")
            return None

        for data_type in list(data_dict.keys()):
            sampling_step = int(np.round(10**9 / data_dict[data_type]))
            for i in range(self.window_size * data_dict[data_type]):
                data_point_value = dataset[index + i]
                data_points.append(
                    {"time": self.start_time + sampling_step * i, "data_type": data_type, "window_id": self.window_id, "index": index + i, "value": data_point_value}
                )
            index += self.window_size * data_dict[data_type]
        print(f"Generated window data points with window_id: {self.window_id}")
        self.window_id += 1
        self.start_time += self.window_size * 10**9
        return data_points
