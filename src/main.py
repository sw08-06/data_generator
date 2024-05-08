import os
import time
import requests
from real_time_data import *
from prediction import *
from config import stress_probability_dict, wear_time_dict

def postData(endpoint, data):
    response = requests.post(f"http://localhost:3000{endpoint}", json=data)
    if response.status_code == 200:
        print("Prediction data successfully sent to the API")
    else:
        print("Failed to send prediction data to the API")


def main():
    dataGen = PredictionGenerator(days=28, window_size=60, stress_probability_dict=stress_probability_dict, wear_time_dict=wear_time_dict)
    prediction_points = dataGen.generate_predictions()
    postData("/api/stress-predict", prediction_points)

    dataGenerator = DataGenerator(file_path=os.path.join("data", "testing.h5"), amount_windows=100, stress_ratio=0.5, window_size=60, first_window_id=100000)
    dataGenerator.load_subject_data()
    while True:
        start_time = time.time()
        data_points = dataGenerator.generate_window_data_points()
        if data_points is None:
            print("Real-time data generation finished.")
            break
        postData("/api/stress-generator", data_points)
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)


if __name__ == "__main__":
    main()
