# Data Generator
This repository contains the code for the service responsible for generating mock physiological data.

To install the required packages locally to run the project, use pip with the following command:
```
pip install -r requirements.txt
```

Alternatively, Docker Compose can be used. To run the entire system, the `deployment` repository must first be cloned from the organization. This repository contains the Docker Compose file for running the entire system. Additionally, the other repositories must be cloned for the `frontend`, `data_generator`, `stress_predictor`, and `api` components. After cloning, ensure that all these repositories are placed within the same folder.

## License
This project is licensed under the MIT License.