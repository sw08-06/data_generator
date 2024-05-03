import datetime
import os
import random
import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)


def dataGenerator(window_size):
    data_types = ["bvp", "eda", "temp"]
    data_fs = [64, 4, 4]
    data_lengths = [window_size * fs for fs in data_fs]
    data_points = []

    for data_type in data_types:
        for length in data_lengths:
            for i in range(length):
                random_number = random.random()
                data_points.append(influxdb_client.Point("data").tag("data_type", data_type).tag("index", i).field("value", random_number))
    return data_points


class DataGenerator:
    def __init__(self, data_path, dates, data_types, fs, window_size, prediction_amount):
        """
        Initialize the DataGenerator object.

        Parameters:
        - data_path (str): Path to the data directory.
        - dates (list): List of dates for which data will be generated.
        - data_types (list): List of data types.
        - fs (float): Sampling frequency (Hz).
        """
        self.data_path = data_path
        self.dates = dates
        self.data_types = data_types
        self.fs = fs
        self.window_size = window_size
        self.prediction_amount = prediction_amount


    def create_subject_data(self, subject, start_date, start_window_id):
        with open(os.path.join(self.data_path, "historic", f"{subject}.pkl"), "rb") as file:
                subject_data = pickle.load(file, encoding="latin1")
                print(f"Loaded data for subject: {subject}")
        
        data_lengths = [self.window_size * fs for fs in self.fs]
        data_points = []

        for i in range(self.prediction_amount): # loop from 0 to 79 
            for j, data_type in enumerate(self.data_types): # loop data_types [BVP, EDA, TEMP]
                for k in range(data_lengths[j]): # loop length (3840 or 240)
                    minute = i+1
                    hour = 12
                    if minute == 60:
                        minute = 1
                        hour = 13
                    data_points.append(
                        influxdb_client.Point("data")
                        .tag("data_type", data_type)
                        .tag("window_id", start_window_id + i)
                        .field("value", subject_data["signal"]["wrist"][data_type][(data_lengths[j] * i) + k])) # mangler date
        
        print(len(data_points))
                        
        return data_points

    def historic_data_generator(self):
        path = os.path.join(self.data_path, "historic")

        subjects = [subject for subject in os.listdir(path)]

        for i, subject in subjects:
            start_window_id = self.prediction_amount * i
            subject_data = self.create_subject_data(subject, self.dates[i], start_window_id)


    def real_time_data_generator(self):
        pass


if __name__ == "__main__":
    #data_points = data_generator(window_size=60)
    #write_api.write(bucket=bucket, org=org, record=data_points)
    dataGenerator = DataGenerator(
        data_path = os.path.join("data"),
        data_types = ["BVP", "EDA", "TEMP"],
        fs = [64, 4, 4],
        dates = [0, 1, 2],
        window_size = 60,
        prediction_amount = 80
    )

    data = dataGenerator.create_subject_data("S3", " ", 80)