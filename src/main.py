import os
import random
import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)


class PredictionGenerator:
    def __init__(self, start_unix_time, days, window_size, stress_probability_dict, wear_time_dict):
        self.window_size = window_size
        self.days = days
        self.start_unix_time = start_unix_time  # format: 1712181600 (4/4/24 00:00:00)
        self.end_unix_time = start_unix_time + days * 86400
        self.stress_probability_dict = stress_probability_dict
        self.wear_time_dict = wear_time_dict
        self.predictions = []

    def generate_predictions(self):
        predictions = []
        current_time = self.start_day
        while current_time < self.end_day:
            wear_mode = self.random_wear_mode()
            current_time += self.wear_time_dict(wear_mode)
            if not wear_mode == "not_wear":
                for _ in range(wear_time_dict(wear_mode) / self.window_size):
                    hour_interval = self.find_hour_interval(current_time)
                    predictions.append(self.calculate_prediction(self.determine_weekend_or_week_day(current_time), hour_interval))
                    current_time += self.window_size
                if wear_mode == "work_hours":
                    current_time += self.wear_time_dict(wear_mode)
        self.predictions = predictions

    def random_wear_mode():
        random_number = random.random()

        if random_number < 0.6:
            return "work_day"
        elif random_number < 0.8:
            return "all_day"
        else:
            return "not_wear"

    def find_hour_interval(self, current_time):
        hour = datetime.fromtimestamp(current_time).hour
        lower = 3 * (hour // 3)
        upper = lower + 3
        return f"{lower}-{upper}"

    def determine_weekend_or_week_day(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return "weekend" if date.weekday() in [5, 6] else "week_day"

    def calculate_prediction(self, weekend_or_weekday, hour_interval):
        return 1 if random.random() < self.stress_probability_dict[weekend_or_weekday][hour_interval] else 0


# def write_data(data):
#   for data_points in data():
#        write_api.write(bucket=bucket, org=org, record=data_points)


# write_data(data)
if __name__ == "__main__":
    stress_probability_dict = {
        "weekend": {
            "0-3": 0.02,
            "3-6": 0.02,
            "6-9": 0.02,
            "9-12": 0.1,
            "12-15": 0.1,
            "15-18": 0.1,
            "18-21": 0.02,
            "21-24": 0.02,
        },
        "weekday": {
            "0-3": 0.05,
            "3-6": 0.05,
            "6-9": 0.5,
            "9-12": 0.4,
            "12-15": 0.3,
            "15-18": 0.2,
            "18-21": 0.1,
            "21-24": 0.05,
        },
    }
    wear_time_dict = {"work_day": 28800, "all_day": 0, "not_wear": 86400}

    dataGen = PredictionGenerator(start_day=1712181600, days=28, window_size=60, stress_probability_dict=stress_probability_dict, wear_time_dict=wear_time_dict)
