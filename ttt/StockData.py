
api_key = 'B9KY7ZHBX1HNKGHO'


from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import datetime

class StockData():
    '''
    Stock data class provides static methods for obtaining data about stocks and crypto.
    Intended for encapsulating the API call.
    '''

    @staticmethod
    def getValues(symbol, currency='stock'):
        '''
        get the full time series from a given stock or cryptocurrency
        :param symbol: symbol of desired stock or crypto
        :param currency: 'stock' or 'crypto'
        :return: (x,y) x is the dates, and y is the stock value
        '''
        if currency=='stock':
            ts = TimeSeries(key=api_key, output_format='pandas')
            try:
                data, meta_data = ts.get_weekly(symbol)
            except KeyError:
                return None, None
            x=data.index.values # get index values (dates)
            y=data.iloc[:,3].values    # get third column which is closing price
            return x,y
        elif currency=='crypto':
            cc = CryptoCurrencies(key=api_key, output_format='pandas')
            try:
                data, meta_data = cc.get_digital_currency_weekly(symbol, market='USD')
            except KeyError:
                return None, None
            x=data.index.values # get index values (dates)
            y=data.iloc[:,3].values    # get third column which is closing price
            return x,y

    @staticmethod
    def getForecast(dates, values, num_predictions=100):
        '''
        get the full time series from a given stock or cryptocurrency
        :param symbol: symbol of desired stock or crypto
        :param currency: 'stock' or 'crypto'
        :return: (x,y) x is the dates, and y is the stock value
        '''

        date_format = '%Y-%m-%d'

        holt = ExponentialSmoothing(values, seasonal_periods=4, trend='add', seasonal='add').fit()
        prediction_values = holt.forecast(num_predictions)

        last_stock_date = datetime.datetime.strptime(dates[-1], date_format)
        prediction_dates =[]
        for i in range(num_predictions):
            prediction_dates.append((last_stock_date+datetime.timedelta(days=(7*i))).strftime(date_format))

        return prediction_dates, prediction_values

    @staticmethod
    def getCurrentPrice(symbol, currency='stock'):
        '''
        get current price for a given stock or cryptocurrency
        :param symbol: string of the desired stock or cryptocurrency
        :param currency: 'stock' or 'crypto'
        :return: (x,y) x is string with date and time, and y is stock value
        '''
        if currency=='stock':
            ts = TimeSeries(key=api_key, output_format='pandas')
            try:
                data, meta_data = ts.get_intraday(symbol, interval='1min', outputsize='compact')
            except KeyError:
                return None, None
            x=data.index.values[-1] # get index values (dates)
            y=data.iloc[-1,3]    # get third column which is closing price
            return x,y
        elif currency=='crypto':
            cc = CryptoCurrencies(key=api_key, output_format='pandas')
            try:
                data, meta_data = cc.get_digital_currency_daily(symbol, market='USD')
            except KeyError:
                return None, None
            x=data.index.values[-1] # get index values (dates)
            y=data.iloc[-1,3]    # get third column which is closing price
            return x,y
