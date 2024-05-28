import unittest
import pandas as pd
import sqlalchemy as sa
from darts import TimeSeries
from darts.models import FFT
import matplotlib.pyplot as plt

class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.engine = sa.create_engine('mysql+mysqlconnector://root:SQLw1tchery@127.0.0.1:3306/weather')
        self.columns_for_prediction = ["temperature", "precipitation", "wind_gust", "pressure"]
        self.df = pd.read_sql_table('weather_data', con=self.engine)
        self.df['date'] = pd.to_datetime(self.df['date'], format='%Y%m%dT%H%M')


    def test_prediction_temperature(self):
        self._test_parameter("temperature")

    def test_prediction_precipitation(self):
        self._test_parameter("precipitation")

    def test_prediction_wind_gust(self):
        self._test_parameter("wind_gust")

    def test_prediction_pressure(self):
        self._test_parameter("pressure")

    # Перевірка похибки у передбаченнях
    def _test_parameter(self, parameter):
        series = TimeSeries.from_dataframe(self.df, 'date', parameter, fill_missing_dates=True, freq=None)
        model = FFT(trend="poly", required_matches=set(), nr_freqs_to_keep=None, trend_poly_degree=1)
        model.fit(series)
        prediction = model.predict(int(365.25 * 24 * 1))
        
        slice_series = series.values()[:100]
        slice_prediction = prediction.values()[:100]

        differences = [pred - ser for pred, ser in zip(slice_prediction, slice_series)]

        for diff in differences:
            self.assertLessEqual(abs(diff), 2.5, msg="Difference between series and prediction is too high") # число є максимально допустимою похибкою

if __name__ == '__main__':
    unittest.main()