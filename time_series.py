from alpha_vantage.timeseries import TimeSeries

def timeSeries(symbol):
    sym = symbol
    ts = TimeSeries(key='Y68D1D2NCXF6K7H2', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=sym,interval='1min', outputsize='full')
    print("Stock data for " , sym , ": ")
    print(data.head(2))

#test case
#x = input("Enter ticker: ")
#timeSeries(x)
