import requests
from config import API_URL


def post_data(endpoint, data):
    response = requests.post(f"{API_URL}{endpoint}", json=data)
    if response.status_code == 200:
        print("Prediction data successfully sent to the API")
    else:
        print("Failed to send prediction data to the API")
