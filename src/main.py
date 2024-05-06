import os
import time
import random
import numpy as np
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")


def data_generator(window_size):
    data_dict = {"bvp": 64, "eda": 4, "temp": 4}
    data_points = []

    for data_type in list(data_dict.keys()):
        sampling_step = int(np.round(1000000000 / data_dict[data_type]))
        for i in range(window_size * data_dict[data_type]):
            random_number = random.random()
            data_points.append(
                influxdb_client.Point("data")
                .time(time.time_ns() + sampling_step * i)
                .tag("data_type", data_type)
                .field("window_id", 1)
                .field("index", i)
                .field("value", random_number)
            )

    return data_points


if __name__ == "__main__":
    time.sleep(5)

    data_points = data_generator(60)

    with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=data_points)
