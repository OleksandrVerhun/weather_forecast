# Weather Data Project

This project is designed to fetch weather data from an open API, process the data, and store it in an AWS S3 bucket / Database. It utilizes libraries such as `requests` for API calls, `pandas` for data manipulation, `boto3` for interaction with AWS services, and `psycopg2` for working with Database.

## Features

- Fetch weather data from a public API.
- Create and clean a DataFrame with the fetched weather data.
- Store the processed data in an AWS S3 bucket / Database.
- Append new data to existing data in the S3 bucket / Database.

## Requirements

To run this project, you will need to install the necessary dependencies. The required libraries are listed in `requirements.txt`.

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/OleksandrVerhun/weather_forecast
   cd <your-repo-directory>

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt

### Usage

1. Ensure you have the correct AWS / Database credentials set in a config.py file:

2. Run the main script:
    ```bash
    python weather_AWS.py
    python weather_DB.py
