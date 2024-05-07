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

    data_points = data_generator(60)

    with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=data_points)
