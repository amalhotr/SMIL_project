from iexfinance.stocks import Stock

def getQuote(symbol):
	return Stock(symbol).get_quote()

def getKeyStats(symbol):
	return Stock(symbol).get_key_stats()