import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import matplotlib
import matplotlib.pyplot as plt
import datetime
from api_key import api_key

####
#### Work in progress


class StockData:
    def __init__(self):
        self.api_key = api_key
        self.df = {}
        # self.today = pd.Timestamp(datetime.date.today())

    def indicator(self):
        # calculate total pv, total volume and VMAP
        self.df['6. pv total'] = (
            ((self.df['2. high'] + self.df['3. low'] + self.df['4. close']) / 3) * self.df['5. volume']).cumsum()
        self.df['7. volume total'] = self.df['5. volume'].cumsum()
        self.df['8. VWAP'] = self.df['6. pv total'] / \
            self.df['7. volume total']

    def clean_data(self):
        # return yesterday's data
        yesterday = pd.Timestamp(
            datetime.date.today() - datetime.timedelta(days=1))
        print(str(yesterday))
        self.df = self.df[self.df.index > yesterday
                          ].sort_index(ascending=False)
        print('data cleaned!')

    def TimeSeries(self, plot=False):
        ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.df, meta_data = ts.get_intraday(
            symbol='MSFT', interval='1min', outputsize='full')

        print('dataframe created')
        self.clean_data()
        self.indicator()
        self.df = self.df.drop(['2. high', '3. low', '5. volume',
                                '6. pv total', '7. volume total'], axis=1)
        print(self.df)
        self.df.plot()
        plt.title('Intraday Time Series (1 min)')
        plt.grid()
        plt.show()

        # if plot == True:


df = StockData()
df.TimeSeries(plot=True)
