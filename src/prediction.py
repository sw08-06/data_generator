import random
from datetime import datetime
import influxdb_client


class PredictionGenerator:
    def __init__(self, start_unix_time, days, window_size, stress_probability_dict, wear_time_dict):
        self.window_size = window_size
        self.days = days
        self.start_unix_time = start_unix_time
        self.end_unix_time = start_unix_time + days * 86400
        self.stress_probability_dict = stress_probability_dict
        self.wear_time_dict = wear_time_dict
        self.prediction_points = []

    def generate_predictions(self):
        window_id = 0
        current_time = self.start_day
        while current_time < self.end_day:
            wear_mode = self.random_wear_mode()
            current_time += self.wear_time_dict(wear_mode)
            if not wear_mode == "not_wear":
                for i in range(self.wear_time_dict(wear_mode) / self.window_size):
                    hour_interval = self.find_hour_interval(current_time)
                    prediction = self.calculate_prediction(self.determine_weekend_or_week_day(current_time), hour_interval)
                    self.prediction_points.append(influxdb_client.Point("prediction").time(current_time).field("window_id", window_id).field("value", prediction))
                    current_time += self.window_size
                    window_id += i
                if wear_mode == "work_hours":
                    current_time += self.wear_time_dict(wear_mode)
        return self.prediction_points

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
