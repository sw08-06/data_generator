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


class DataGenerator:
    def __init__(self, start_day, days, window_size, stress_probability_dict):
        self.window_size = window_size
        self.days = days
        self.start_day = start_day  # format: 1712181600 (4/4/24 00:00:00)
        self.stress_probability_dict = stress_probability_dict

        self.dates = []
        for i in range(self.days):
            self.dates.append(self.start_day + (86400 * i))  # 86400 = 1 day in seconds

    def generate_predictions(self):
        for i in range(self.days):
            wear_probability = self.wear_probability()
            if wear_probability == "work_hours":
                self.dates[i] += 28800  # Add 8 hours
                for j in range(28800 / self.window_size):  # Predict from 8:00 - 16:00
                    
                    # add 1 minute

                    # elif(wear_probability == "all_day"):
                    # for j in range(1440): # Predict from 00:00 - 24:00
                    # generate prediction
                    # add 1 minute
                    continue
            else:
                continue

    def stress_probability(self, timestamp):
        hour = datetime.fromtimestamp(timestamp).hour
        random_number = random.random()
        

    def wear_probability():
        random_number = random.random()

        if random_number < 0.6:
            return "work_hours"
        elif random_number < 0.8:
            return "all_day"
        else:
            return "not_wear"

    def is_weekend(self, timestamp):
        date = datetime.fromtimestamp(timestamp)

        return date.weekday() in [5, 6]


# def write_data(data):
#   for data_points in data():
#        write_api.write(bucket=bucket, org=org, record=data_points)


# write_data(data)
if __name__ == "__main__":
    stress_probabilty_dict = {
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

    dataGen = DataGenerator(start_day=1712181600, days=28, window_size=60, stress_probability_dict=stress_probabilty_dict)
