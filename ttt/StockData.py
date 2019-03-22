
api_key = 'B9KY7ZHBX1HNKGHO'
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies

import pandas

class StockData():

    @staticmethod
    def getValues(symbol, currency='stock'):
        ''' get the full time series from a given stock or cryptocurrency
            param symbol: symbol of desired stock or crypto
            param currency: 'stock' or 'crypto' '''
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

    @staticmethod
    def getCurrentPrice(symbol, currency='stock'):
        ''' get current price for a given stock or cryptocurrency
            param symbol: string of the desired stock or cryptocurrency
            param currency: 'stock' or 'crypto' 
            return tuple(x,y) x is string with date and time
                                y is the stock/crypto value '''
        if currency=='stock':
            ts = TimeSeries(key=api_key, output_format='pandas')
            try:
                data, meta_data = ts.get_weekly(symbol)
            except KeyError:
                return None, None
            x=data.index.values[-1] # get index values (dates)
            y=data.iloc[-1,3]    # get third column which is closing price
            return x,y
        elif currency=='crypto':
            cc = CryptoCurrencies(key=api_key, output_format='pandas')
            try:
                data, meta_data = cc.get_digital_currency_weekly(symbol, market='USD')
            except KeyError:
                return None, None
            x=data.index.values[-1] # get index values (dates)
            y=data.iloc[-1,3]    # get third column which is closing price
            return x,y
