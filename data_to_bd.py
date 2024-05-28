import pandas as pd
import sqlalchemy as sa

def data_migrator():
    connection_string = 'mysql+mysqlconnector://root:SQLw1tchery@127.0.0.1:3306/weather'
    engine = sa.create_engine(connection_string)
    
    headers = ["date", "temperature", "precipitation", "wind_gust", "cloud_cover", "pressure"]
    df = pd.read_csv('Weather_Forecast\\dataexport_20240417T145023.csv', skiprows=10, header=None, names=headers, low_memory=False)
    
    df['temperature'] = df['temperature'].astype('float32')
    df['precipitation'] = df['precipitation'].astype('float32')
    df['wind_gust'] = df['wind_gust'].astype('float32')
    df['cloud_cover'] = df['cloud_cover'].astype('int8')
    df['pressure'] = df['pressure'].astype('float32')
    
    df = df.dropna(subset=['temperature', "precipitation", "wind_gust", "cloud_cover", "pressure"])
    df.to_sql(con=engine, name="weather_data", if_exists='replace', index=False)
    
    print("База даних оновлена!")