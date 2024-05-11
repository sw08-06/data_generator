# Data Generator
This repository contains the code for the service responsible for generating mock physiological data.

To install the required packages locally to run the project, use pip with the following command:
```
pip install -r requirements.txt
```

Alternatively, Docker Compose can be used to start up two services. An InfluxDB service and a data generator service. To do this create a `.env` file in the project root directory and populate it with the following environment variables:
```
INFLUX_USERNAME="USERNAME"
INFLUX_PASSWORD="PASSWORD"
INFLUX_BUCKET="BUCKET"
INFLUX_ORG="ORG"
INFLUX_TOKEN="TOKEN"
INFLUX_URL="http://IP_ADDRESS_OF_HOST_MACHINE:8086"
```
Ensure to replace `"USERNAME"`, `"PASSWORD"`, `"BUCKET"`, `"ORG"`, `"TOKEN"`, and `"IP_ADDRESS_OF_HOST_MACHINE"` with your actual InfluxDB credentials and server information.

Then, run the following command in the terminal:
```
docker-compose up -d
```