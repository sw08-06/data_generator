import time
import random
from datetime import datetime, timezone
import numpy as np
import influxdb_client


class PredictionGenerator:
    def __init__(self, days, window_size, stress_probability_dict, wear_time_dict):
        self.window_size = window_size * 10**9
        self.days = days
        time_now_seconds = np.round(time.time())
        self.start_time_ns = (time_now_seconds - time_now_seconds % 86400 - ((days) * 86400)) * 10**9
        self.end_time_ns = (time_now_seconds - time_now_seconds % 86400) * 10**9
        self.stress_probability_dict = stress_probability_dict
        self.wear_time_dict = wear_time_dict
        self.prediction_points = []

    def generate_predictions(self):
        window_id = 0
        current_time = self.start_time_ns
        while current_time < self.end_time_ns:
            wear_mode = self.random_wear_mode()
            if wear_mode == "not_wear":
                current_time += 86400 * 10**9
            else:
                if wear_mode == "work_day":
                    current_time += 28800 * 10**9
                for i in range(int(self.wear_time_dict[wear_mode] / self.window_size)):
                    hour_interval = self.find_hour_interval(current_time)
                    prediction = self.calculate_prediction(self.determine_weekend_or_weekday(current_time), hour_interval)
                    self.prediction_points.append(
                        influxdb_client.Point("prediction").time(self.format_timestamp(current_time)).field("window_id", window_id).field("value", prediction)
                    )
                    current_time += self.window_size
                    window_id += 1
                if wear_mode == "work_day":
                    current_time += 28800 * 10**9
        print(f"{len(self.prediction_points)} prediction points generated. Highest window_id: {window_id - 1}")
        return self.prediction_points

    def random_wear_mode(self):
        random_number = random.random()

        if random_number < 0.6:
            return "work_day"
        elif random_number < 0.8:
            return "all_day"
        else:
            return "not_wear"

    def find_hour_interval(self, current_time):
        hour = datetime.fromtimestamp(current_time / 10**9).hour
        lower = 3 * (hour // 3)
        upper = lower + 3
        return f"{lower}-{upper}"

    def determine_weekend_or_weekday(self, timestamp):
        date = datetime.fromtimestamp(timestamp / 10**9)
        return "weekend" if date.weekday() in [5, 6] else "weekday"

    def calculate_prediction(self, weekend_or_weekday, hour_interval):
        return 1 if random.random() < self.stress_probability_dict[weekend_or_weekday][hour_interval] else 0

    def format_timestamp(self, time_nano):
        dt = datetime.fromtimestamp(time_nano / 1e9, timezone.utc)
        return "{}{:03.0f}".format(dt.strftime("%Y-%m-%dT%H:%M:%S.%f"), time_nano % 1e3)
