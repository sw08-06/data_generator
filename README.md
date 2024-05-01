# Data Generator
This repository contains the code for the service that is responsible for generating mock physiological data.

To install the required packages to run the project, use pip with the following command:
```
pip install -r requirements.txt
```
Alternatively, use docker-compose:
```
docker-compose up -d
```

### .env
Make a .env file with the following:
```
INFLUX_USERNAME="USERNAME"
INFLUX_PASSWORD="PASSWORD"
INFLUX_BUCKET="BUCKET"
INFLUX_ORG="ORG"
INFLUX_TOKEN="TOKEN"
INFLUX_URL="http://IP_ADDRESS_OF_HOST_MACHINE:8086"
```