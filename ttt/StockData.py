
api_key = 'B9KY7ZHBX1HNKGHO'


from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas
import pygal

class StockData():
    @staticmethod
    def test(str):
        print(str) 

    @staticmethod
    def getValues():
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_weekly(symbol='MSFT')
        x=data.index.values # get index values (dates)
        y=data.iloc[:,3]    # get third column which is closing price
        return x,y
