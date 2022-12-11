from utils.db import execute
from datetime import datetime


async def db_inserir_dados(data):
    query = """insert into data(humidity, celsius, fahrenheit, heatindexcelsius, heatindexfahrenheit, airquality, alarmset, date) 
            values(:humidity, :celsius, :fahrenheit, :heatindexcelsius, :heatindexfahrenheit, :airquality, :alarmset, :date)"""

    values = {"humidity": float(data['humidity']), "celsius": float(data['celsius']), "fahrenheit": float(data['fahrenheit']), "heatindexcelsius": float(data['heatindexcelsius']), "heatindexfahrenheit": float(data['heatindexfahrenheit']),
    "airquality": int(data['airquality']), "alarmset": int(data['alarmset']), "date": datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%f')}

    try:
        await execute(query, False, values)
    except Exception as e:
        raise e

async def db_create_table_if_not_exists():
    query = """CREATE TABLE IF NOT EXISTS data (humidity NUMERIC(5, 1) NOT NULL, celsius NUMERIC(5, 1) NOT NULL, fahrenheit NUMERIC(5, 1) NOT NULL, heatindexcelsius NUMERIC(5, 1) NOT NULL, heatindexfahrenheit NUMERIC(5, 1) NOT NULL, airquality integer NOT NULL, alarmset integer NOT NULL, date timestamp NOT NULL) """

    values = None

    try:
        await execute(query, False, values)
    except Exception as e:
        raise e