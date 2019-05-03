import uuid 

from datetime import datetime, date
from decimal import Decimal
from .iex import getQuote
from .models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction, Portfolio, Holding

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay, USThanksgivingDay

class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]

def get_trading_close_holidays(year):
    inst = USTradingCalendar()
    return inst.holidays(datetime(year-1, 12, 31), datetime(year, 12, 31))


def buy(price, pendTrans):
	total = price*pendTrans.quantity
	try:
		portfolio = Portfolio.objects.get(player=pendTrans.player, league=pendTrans.league)
	except:
		portfolio = Portfolio(id=uuid.uuid4(),player=pendTrans.player, league=pendTrans.league,cash=pendTrans.league.startingBalance)

	if portfolio.cash >= total:
		portfolio.cash = portfolio.cash - Decimal(total)
		portfolio.save()
		holdingInstance = Holding(id=uuid.uuid4(), ticker=pendTrans.ticker, price=price, quantity=pendTrans.quantity,portfolio=portfolio)
		holdingInstance.save()
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='f', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=price, quantity=pendTrans.quantity, total=total)
		transactionHistoryInstance.save()

	else:
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='c', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=price, quantity=pendTrans.quantity, total=total)
		transactionHistoryInstance.save()
	
	pendTrans.delete()

	return

def sell(price, pendTrans):
	total = price*pendTrans.quantity
	portfolio = Portfolio.objects.get(player=pendTrans.player, league=pendTrans.league)
	holdings = Holding.objects.filter(ticker=pendTrans.ticker, portfolio=portfolio.id).order_by('price')

	holdingQuantity = 0
	for holding in holdings:
		holdingQuantity = holdingQuantity + holding.quantity

	if holdingQuantity >= pendTrans.quantity:
		
		tradeQuantity = pendTrans.quantity
		for holding in holdings:
			if holding.quantity > tradeQuantity:
				holding.quantity = holding.quantity - tradeQuantity
				holding.save()
				tradeQuantity = 0 
				break
			else:
				tradeQuantity = tradeQuantity - holding.quantity
				holding.delete()

		portfolio.cash = portfolio.cash + Decimal(total)
		portfolio.save()
		
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='f', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=price, quantity=pendTrans.quantity, total=total)
		transactionHistoryInstance.save()

	else:
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='c', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=price, quantity=pendTrans.quantity, total=total)
		transactionHistoryInstance.save()

	pendTrans.delete()

	return

def transaction(pendTrans):
	if pendTrans.asset.name == 'Cryptocurrency':
		quote = getQuote(pendTrans.ticker + 'USDT')
	else:
		quote = getQuote(pendTrans.ticker)

	price = quote['latestPrice']

	if pendTrans.transactionType.name == 'Market Buy':
		buy(price, pendTrans)
	
	elif pendTrans.transactionType.name == 'Market Sell':
		sell(price, pendTrans)
	
	elif pendTrans.transactionType.name == 'Limit Buy':
		if price <= pendTrans.price1:
			buy(price, pendTrans)
	
	elif pendTrans.transactionType.name == 'Limit Sell':
		if price >= pendTrans.price1:
			sell(price, pendTrans)

	elif pendTrans.transactionType.name == 'Stop Limit':
		if price >= pendTrans.price1:
			instance = PendingTransaction(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=TransactionType.objects.get(name='Limit Buy'), timeInForce=pendTrans.timeInForce, transactionStatus='q', submittedDateTime=datetime.now(), price1=pendTrans.price2, quantity=pendTrans.quantity)
			instance.save()
			pendTrans.delete()

	elif pendTrans.transactionType.name == 'Stop Loss':
		if price <= pendTrans.price1:
			instance = PendingTransaction(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=TransactionType.objects.get(name='Limit Sell'), timeInForce=pendTrans.timeInForce, transactionStatus='q', submittedDateTime=datetime.now(), price1=pendTrans.price2, quantity=pendTrans.quantity)
			instance.save()
			pendTrans.delete()
	return

def cryptoExecute():
	pendingTransactions = PendingTransaction.objects.filter(asset=Asset.objects.get(name='Cryptocurrency'))
	
	for pendTrans in pendingTransactions:
		pendTrans.transactionStatus='p'
		transaction(pendTrans)

	return


def stockMarketExecute():
	now = datetime.today().date()
	holidays = []
	for x in get_trading_close_holidays(datetime.today().year):
		holidays.append(x.date())

	if now in holidays:
		return
	else:
		pendingTransactions = PendingTransaction.objects.filter(asset=Asset.objects.get(name='Stock'))

		for pendTrans in pendingTransactions:
			pendTrans.transactionStatus='p'
			transaction(pendTrans)
		return

def pendDayDelete():
	PendingTransaction.objects.filter(timeInForce=TimeInForce.objects.get(name='Good-for-day')).delete()

	return