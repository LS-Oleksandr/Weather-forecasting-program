import pandas as pd
import sqlalchemy as sa
from darts import TimeSeries
from darts.models import FFT
import matplotlib.pyplot as plt

def train_and_plot(year, parameter):

    engine = sa.create_engine('mysql+mysqlconnector://root:SQLw1tchery@127.0.0.1:3306/weather')
    columns_for_prediction = ["temperature", "precipitation", "wind_gust", "pressure"]

    df = pd.read_sql_table('weather_data', con = engine)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%dT%H%M')

    series = TimeSeries.from_dataframe(df, 'date', parameter, fill_missing_dates=True, freq=None)
    
    model = FFT(trend="poly", required_matches=set(), nr_freqs_to_keep=None, trend_poly_degree=1)
    model.fit(series)
    prediction = model.predict(int(365.25 * 24 * year))
    
    time_difference = series.time_index[0] - prediction.time_index[0]
    
    shifted_prediction_time_index = prediction.time_index + time_difference
    
    plt.figure(figsize=(12, 6))
    plt.plot(series.time_index, series.values(), label="Train data", color="#5B2C6F")
    plt.plot(shifted_prediction_time_index, prediction.values(), label="Prediction data", color="#1ABC9C")
    plt.legend()
    plt.title(f"{parameter} Prediction")
    plt.xlabel("Date")
    plt.ylabel(parameter.capitalize())

    plt.show()