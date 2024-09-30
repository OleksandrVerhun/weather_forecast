# Weather Data Project

![test](https://cdn.leonardo.ai/users/b87de89e-86aa-4d10-8a2d-5f38a33fbc5d/generations/abcbc0f9-0c8a-4a6e-8baa-b0d56de2e105/Leonardo_Vision_XL_Create_an_illustration_with_a_central_cloud_3.jpg)

This project is designed to retrieve weather data from an open API, process the data and store it in an AWS S3 bucket or Database, depending on what you need. It uses libraries such as `requests` for API calls, `pandas` for data manipulation, `boto3` for interacting with AWS services and `psycopg2` for working with Database.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Start the program](#start-the-program)
  - [AWS](#aws)
  - [PostgreSQL](#postgresql)
- [Running with Docker](#running-with-docker)
- [License](#license)

## Features

- Fetch weather data from a public API.
- Create and clean a DataFrame with the fetched weather data.
- Store the processed data in an AWS S3 bucket or Database.
- Append new data to existing data in the S3 bucket or Database.

## Requirements

- Python 3.10
- Docker, Docker Compose (if needed)
- PostgreSQL or AWS account

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OleksandrVerhun/weather_forecast
   cd <your-repo-directory>

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt

3. Customize the configuration file (config.py) with your parameters (API_KEY, AWS_ACCESS_KEY, etc.).

## Start the program

### AWS

1. Make sure you have your AWS credentials set up.
2. Use AWS Lambda or EC2 to deploy your application.
3. To test you can run the main script:
      ```bash
      python weather_aws.py

### PostgreSQL

1. Start the PostgreSQL server locally or using Docker.
2. Create a database (do not forget to specify its name and other data in config.py)
3. Run the main script:
      ```bash
      python weather_db.py

## Running with Docker

1. Change the credentials in the docker-compose.yml file
2. Open PowerShell or a command prompt.
3. Go to the project catalog:
      ```bash
      cd <directory>
4. Run Docker Compose:
      ```bash
      docker-compose up --build
5. Go to http://localhost:8080 to access pgAdmin.

## License
- Distributed under the [MIT License](https://choosealicense.com/licenses/mit/). See LICENSE.txt for more information.