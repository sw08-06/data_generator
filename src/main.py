import os
import random
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


def data_generator(window_size):
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


data_points = data_generator(window_size=60)
write_api.write(bucket=bucket, org=org, record=data_points)
