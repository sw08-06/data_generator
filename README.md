# Data Generator
This repository houses the code for a service responsible for generating mock physiological data.

## Installation
To set up the project, ensure you have Python and Docker installed on your machine.

### Requirements Installation
To install the required Python packages, execute the following command in your terminal:
```
pip install -r requirements.txt
```

### Docker Installation
Alternatively, you can use Docker Compose. Run the following command in your terminal:
```
docker-compose up -d
```

## Environment Setup
Create a `.env` file in the project root directory and populate it with the following environment variables:
```
INFLUX_USERNAME="USERNAME"
INFLUX_PASSWORD="PASSWORD"
INFLUX_BUCKET="BUCKET"
INFLUX_ORG="ORG"
INFLUX_TOKEN="TOKEN"
INFLUX_URL="http://IP_ADDRESS_OF_HOST_MACHINE:8086"
```
Ensure to replace `"USERNAME"`, `"PASSWORD"`, `"BUCKET"`, `"ORG"`, `"TOKEN"`, and `"IP_ADDRESS_OF_HOST_MACHINE"` with your actual InfluxDB credentials and server information.
