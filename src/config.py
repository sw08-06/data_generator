import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

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

wear_time_dict = {"work_day": 28800 * 10**9, "all_day": 86400 * 10**9, "not_wear": 0}
