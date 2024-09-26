import requests
import pandas as pd
import boto3
from config import *


def call_api():
    try:     
        response = requests.get(API_CALL)
        weather_data = response.json()
    except Exception as e:
        print(e)

    print(f"API call was successful")
    return weather_data


def create_df(weather_data):
    columns = ['continent', 'country', 'town', 'time', 'condition', 'temperature_c', 'precipitation_mm', 'cloud_percentage', 'humidity', 'wind_kph', 'pressure_mb']
    df = pd.DataFrame(columns=columns)

    new_row = {
        'continent': weather_data['location']['tz_id'],
        'country': weather_data['location']['country'],
        'town': weather_data['location']['name'],
        'time': weather_data['location']['localtime'],
        'condition': weather_data['current']['condition']['text'],
        'temperature_c': weather_data['current']['temp_c'],
        'precipitation_mm': weather_data['current']['precip_mm'],
        'cloud_percentage': weather_data['current']['cloud'],
        'humidity': weather_data['current']['humidity'],
        'wind_kph': weather_data['current']['wind_kph'],
        'pressure_mb': weather_data['current']['pressure_mb']
    }

    df.loc[len(df)] = new_row

    print(f"Created DataFrame with new data")
    return df


def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()

    # df['temperature_c'] = pd.to_numeric(df['temperature_c'], errors='coerce')
    # df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    # df['wind_kph'] = pd.to_numeric(df['wind_kph'], errors='coerce')

    print(f"Cleaned new data")

    return df


def get_s3_client():
    try:
        s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION_NAME)
    except Exception as e:
        print(e)

    print(f"Connected to S3")
    return s3


def download_from_s3(s3_client, bucket, object_path):
    try:
        s3_client.download_file(bucket, object_path, OBJECT_NAME)
        # Creating DataFrame from S3
        existing_df = pd.read_csv(OBJECT_NAME)
        print(f"File {OBJECT_NAME} downloaded successfully from {bucket}/{object_path}")
        return existing_df
    except Exception as e:
        print(e)
        return pd.DataFrame()


def upload_to_s3(s3_client, bucket, object_path):
    try:
        s3_client.upload_file(OBJECT_NAME, bucket, object_path)
        print(f"File {OBJECT_NAME} uploaded successfully to {bucket}/{object_path}.")
    except Exception as e:
        print(e)


def append_data_to_s3(s3_client, bucket, new_data, object_path):    
    # Downloading existing data from S3
    existing_data_df = download_from_s3(s3_client, bucket, object_path)

    # Combine existing data with new data
    updated_df = pd.concat([existing_data_df, new_data], ignore_index=True)

    # Create CSV file
    updated_df.to_csv(OBJECT_NAME, index=False)

    # Upload this file to S3
    upload_to_s3(s3_client, bucket, object_path)


def main():
    weather_data = call_api()
    new_data = create_df(weather_data)
    cleaned_data = clean_data(new_data)
    s3_client = get_s3_client()
    append_data_to_s3(s3_client, AWS_BUCKET_NAME, cleaned_data, f"weather/{OBJECT_NAME}")


if __name__ == "__main__":
    main()