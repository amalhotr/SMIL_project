#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 antoni <antoni@antoni>
#
# Distributed under terms of the MIT license.

api_key = 'B9KY7ZHBX1HNKGHO'


from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pygal

class StockData():
    @staticmethod
    def test(str):
        print(str)

    @staticmethod
    def getValues():
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_weekly(symbol='MSFT')
        x=data.index.values
        y=data.iloc[:,3]    # get third column which is closing price
        return x,y
        
    @staticmethod
    def getX():
        return [0,1,2,3,4]

    @staticmethod
    def getY():
        return [0,1,4,9,16]


    @staticmethod
    def getPlot():
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_weekly(symbol='MSFT')

'''
ts = TimeSeries(key=api_key, output_format='pandas')
cc = CryptoCurrencies(key=api_key, output_format='pandas')

#data, meta_data = ts.get_intraday(symbol='MPGFX', interval='5min',outputsize='full')
data_BTC, meta_data_BTC = cc.get_digital_currency_weekly(symbol='BTC', market='USD')

# plot data at closing
plt.subplot(211)
data_MPFGX['4. close'].plot()
plt.title('MPGFX weekly performance')

# plot data at closing
plt.subplot(212)
data_BTC['4a. close (USD)'].plot()
plt.title('BTC weekly performance')

# get 20 most recent values
# last_20_MPGFX = data.iloc[-20:-1, :]

plt.show()
'''
