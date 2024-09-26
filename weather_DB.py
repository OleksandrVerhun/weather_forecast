import sys
import requests
import pandas as pd
import psycopg2
from config import *


def call_api():
    try:     
        response = requests.get(API_CALL)
        weather_data = response.json()
        print(f"API call was successful")
        return weather_data
    except Exception as e:
        print(f"API call failed\n{e}")
        sys.exit(1)


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


def connet_to_DB():
    try:
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
        )
        cursor = conn.cursor()
        print(f"Connected to the '{DB_NAME}' database")
        return cursor, conn
    except Exception as e:
        print(f"Cannot connect to the '{DB_NAME}' database\n{e}")
        sys.exit(1)


def fetch_data(cursor):
    try:
        cursor.execute(f"SELECT * FROM {DB_TABLE_NAME}")
        all_results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(all_results, columns=columns)
        print(f"Fetched all data from the '{DB_TABLE_NAME}' table")
        return df
    except Exception as e:
        print(f"Cannot fetch data from the '{DB_TABLE_NAME}' table\n{e}")
        sys.exit(1)


def append_data_to_DB(cursor, conn):
    try:
        cursor.execute(f"TRUNCATE TABLE {DB_TABLE_NAME}")

        insert_query = f"""
        INSERT INTO {DB_TABLE_NAME} (continent, country, town, time, condition, temperature_c, precipitation_mm, cloud_percentage, humidity, wind_kph, pressure_mb)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        df = pd.read_csv("weather.csv")

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row['continent'],
                row['country'],
                row['town'],
                row['time'],
                row['condition'],
                row['temperature_c'],
                row['precipitation_mm'],
                row['cloud_percentage'],
                row['humidity'],
                row['wind_kph'],
                row['pressure_mb']
            ))

        conn.commit()
        print(f"Data successfully added to the '{DB_TABLE_NAME}' table")
    except Exception as e:
        print(f"Error adding data to the '{DB_TABLE_NAME}' table\n{e}")
        sys.exit(1)


def main():
    weather_data = call_api()
    new_data = create_df(weather_data)
    cleaned_new_data = clean_data(new_data)
    cursor, conn = connet_to_DB()
    existing_data = fetch_data(cursor)
    updated_df = pd.concat([existing_data, cleaned_new_data], ignore_index=True)
    updated_df.to_csv(OBJECT_NAME, index=False)

    append_data_to_DB(cursor, conn)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()