import os
import time
from real_time_data import *
from prediction import *
from http_requests import *
from config import *


def main():
    time.sleep(10)
    window_size = 60
    dataGen = PredictionGenerator(days=27, window_size=window_size, stress_probability_dict=stress_probability_dict, wear_time_dict=wear_time_dict)
    prediction_points, last_window_id = dataGen.generate_predictions()
    post_data("/api/stress-predict", prediction_points)

    dataGenerator = DataGenerator(file_path=os.path.join("data", "testing.h5"), amount_windows=1, stress_ratio=0.5, window_size=60, first_window_id=last_window_id + 1)
    dataGenerator.load_subject_data()
    while True:
        start_time = time.time()
        data_points = dataGenerator.generate_window_data_points()
        if data_points is None:
            print("Real-time data generation finished.")
            break
        post_data("/api/stress-generator", data_points)
        elapsed_time = time.time() - start_time
        if elapsed_time < window_size:
            time.sleep(window_size - elapsed_time)


if __name__ == "__main__":
    main()
