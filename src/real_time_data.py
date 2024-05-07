import time
import random
import numpy as np
import influxdb_client


def data_generator(window_size, window_id):
    """
    Generates one window of data points.
    Args:
        window_size (int): Size of window in seconds.
    Returns:
        list: List of data points.
    """
    data_dict = {"bvp": 64, "eda": 4, "temp": 4}
    data_points = []

    for data_type in list(data_dict.keys()):
        sampling_step = int(np.round(1000000000 / data_dict[data_type]))
        for i in range(window_size * data_dict[data_type]):
            random_number = random.random()
            data_points.append(
                influxdb_client.Point("data")
                .time(time.time_ns() + sampling_step * i)
                .tag("data_type", data_type)
                .field("window_id", window_id)
                .field("index", i)
                .field("value", random_number)
            )

    return data_points
