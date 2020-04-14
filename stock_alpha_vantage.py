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

# symbol =
# ts = TimeSeries(key=api_key, output_format='pandas')
# dataframe, meta_data = ts.get_intraday(
#     symbol='MSFT', interval='1min', outputsize='full')
#     dataframe.to_excel("output.xlsx")

# Create VWAP indicator
# dataframe['6. VWAP'] = 0

# vol = 0
# pv = 0
# # iterate through rows reversed
# for index, row in dataframe.iloc[::-1].iterrows():
#     vol = vol + row['5. volume']
#     pv = pv + (((row['2. high'] + row['3. low'] +
#                  row['4. close']) / 3) * row['5. volume'])

#     vwap = pv / vol

#     dataframe.at[index, '6. VWAP'] = vwap


# dataframe.to_excel("output.xlsx")
# dataframe = dataframe.drop('5. volume', 1)
# dataframe.plot()
# plt.title('Intraday Time Series for the xxxx stock (1 min)')
# plt.grid()
# plt.show()

# i = 1
# while i == 1:
#     data, meta_data = ts.get_intraday(
#         symbol='MSFT', interval='1min', outputsize='compact')
#     data.to_excel("output.xlsx")
#     time.sleep(60)
#     break

# close_data = data['4. close']
# percentage_change = close_data.pct_change()

# print(percentage_change)

# last_change = percentage_change[-1]

# if abs(last_change) > 0.0004:
#     print("MSFT Alert:" + str(last_change))
