import requests
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from config import API_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET

client = influxdb_client.InfluxDBClient(url=API_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


def post_data(endpoint, data):
    print(f"{API_URL}{endpoint}")
    response = requests.post(f"{API_URL}{endpoint}", json=data)
    if response.status_code == 200:
        print("Prediction data successfully sent to the API")
    else:
        print("Failed to send prediction data to the API")
