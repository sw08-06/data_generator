import os
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from real_time_data import *
from prediction import *

load_dotenv()

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


def write_data_influxdb(data):
    with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=data)


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
prediction_points = dataGen.generate_predictions()

write_data_influxdb(prediction_points)

dataGenerator = DataGenerator(data_path=os.path.join("data", "testing.h5"), amount_windows=100, stress_ratio=0.5, window_size=60, first_window_id=0)
dataGenerator.load_subject_data()
while True:
    start_time = time.time()

    data_points = dataGenerator.generate_window_data_points(60)

    write_data_influxdb(data_points)

    elapsed_time = time.time() - start_time

    if elapsed_time < 60:
        time.sleep(60 - elapsed_time)
