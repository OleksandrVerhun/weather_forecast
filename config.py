TOWN = "London"

# api.weatherapi.com
API_KEY = ""
API_CALL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={TOWN}&aqi=no"

# Forecast for several days (not working ;c)
# API_CALL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={town_forecast}&days=7&aqi=no&alerts=no"

OBJECT_NAME = "weather.csv"

# For Database
DB_NAME = ""
DB_TABLE_NAME = ""
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""

# For AWS
AWS_BUCKET_NAME = ""
AWS_ACCESS_KEY = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = ""