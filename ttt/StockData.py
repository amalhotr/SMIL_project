
api_key = 'B9KY7ZHBX1HNKGHO'


from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas

class StockData():

    @staticmethod
    def getValues(symbol, currency='stock'):
        if currency=='stock':
            ts = TimeSeries(key=api_key, output_format='pandas')
            try:
                data, meta_data = ts.get_weekly(symbol)
            except KeyError:
                return None, None
            x=data.index.values # get index values (dates)
            y=data.iloc[:,3]    # get third column which is closing price
            return x,y
        elif currency=='crypto':
            cc = CryptoCurrencies(key=api_key, output_format='pandas')
            try:
                data, meta_data = cc.get_digital_currency_weekly(symbol, market='USD')
            except KeyError:
                return None, None
            x=data.index.values # get index values (dates)
            y=data.iloc[:,3]    # get third column which is closing price
            return x,y
