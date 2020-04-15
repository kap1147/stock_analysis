import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import matplotlib
import matplotlib.pyplot as plt
import datetime
from api_key import api_key

# TODO
# create a queryset method


class StockData:
    def __init__(self):
        self.api_key = api_key
        self.df = {}

   # Add indicators to dataframe
    def indicator(self):
        # VWAP
        # TODO
        # take in a list and loop through
        if True:
            self.df['6. pv total'] = (
                ((self.df['2. high'] + self.df['3. low'] + self.df['4. close']) / 3) * self.df['5. volume']).cumsum()
            self.df['7. volume total'] = self.df['5. volume'].cumsum()
            self.df['8. VWAP'] = self.df['6. pv total'] / \
                self.df['7. volume total']

    def set_queryset(self):
        # TODO
        # a better query method q:
        yesterday = pd.Timestamp(
            datetime.date.today() - datetime.timedelta(days=1))
        self.df = self.df[self.df.index > yesterday
                          ].sort_index(ascending=False)

    def TimeSeries(self, plot=False, to_excel=False):
        ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.df, meta_data = ts.get_intraday(
            symbol='MSFT', interval='1min', outputsize='full')

        print('dataframe created')
        self.set_queryset()
        self.indicator()
        self.df = self.df.drop(['2. high', '3. low', '5. volume',
                                '6. pv total', '7. volume total'], axis=1)

        if plot == True:
            # create plot
            # a lot to do here
            self.df.plot()
            plt.title('Intraday Time Series (1 min)')
            plt.grid()
            plt.show()

        if to_excel == True:
            # create excel file
            # TODO
            # format a better name
            self.df.to_excel("intraday.xlsx")


df = StockData()
df.TimeSeries(plot=True, to_excel=True)
