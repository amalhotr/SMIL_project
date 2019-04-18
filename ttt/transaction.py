import uuid

from datetime import datetime
from .models import TransactionHistory, PendingTransaction, Portfolio, Holding
from .iex import getQuote

def buy(quote, pendTrans):
	total = quote.latestPrice*pendTrans.quantity
	portfolio = Portfolio.objects.get(player=pendTrans.player, league=pendTrans.league)

	if portfolio.cash >= total:
		portfolio.cash = portfolio.cash - total
		portfolio.save()
		holdingInstance = Holding(id=uuid.uuid4(), ticker=pendTrans.ticker, price=quote.latestPrice, quantity=pendTrans.quantity, portfolio=portfolio)
		holdingInstance.save()
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='f', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=quote.latestPrice, quantity=pendTrans.quantity, total=total)
		transactionHistory.save()
		PendingTransaction.objects.get(id=pendTrans.id).delete()
	else:
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='c', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=quote.latestPrice, quantity=pendTrans.quantity, total=total)
		transactionHistory.save()
		PendingTransaction.objects.get(id=pendTrans.id).delete()
	
	return

def sell(quote, pendTrans):
	quote = getQuote(pendTrans.ticker)
	total = quote.latestPrice*pendTrans.quantity
	portfolio = Portfolio.objects.get(player=pendTrans.player, league=pendTrans.league)
	holdings = Holding.objects.filter(ticker=pendTrans.ticker, portfolio=portfolio.id).order_by('price')

	holdingQuantity = 0
	for holding in holdings:
		holdingQuantity = holdingQuantity + holding.quantity 
		
	if holdingQuantity >= pendTrans.quantity:
		for holding in holdings:
			if holdingQuantity >= holding.quantity:
				holdingQuantity = holdingQuantity - holding.quantity
				holding.delete()
			else:
				holding.quantity = holding.quantity - holdingQuantity
				holding.save()
				holdingQuantity = 0
				break

		portfolio.cash = portfolio.cash + total
		portfolio.save()
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='f', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=quote.latestPrice, quantity=pendTrans.quantity, total=total)
			transactionHistory.save()
			PendingTransaction.objects.get(id=pendTrans.id).delete()

	else:
		transactionHistoryInstance = TransactionHistory(id=uuid.uuid4(), player=pendTrans.player, league=pendTrans.league, asset=pendTrans.asset, ticker=pendTrans.ticker, transactionType=pendTrans.transactionType, timeInForce=pendTrans.timeInForce, transactionStatus='c', submittedDateTime=pendTrans.submittedDateTime, fulfilledDateTime=datetime.now(), price1=quote.latestPrice, quantity=pendTrans.quantity, total=total)
		transactionHistory.save()
		PendingTransaction.objects.get(id=pendTrans.id).delete()

	return

def transaction(pendTrans):
	quote = getQuote(pendTrans.ticker)	

	if pendTrans.transactionType == 'Market Buy':
		buy(quote, pendTrans)

	elif pendTrans.transactionType == 'Market Sell':
		sell(quote, pendTrans)

	elif pendTrans.transactionType == 'Limit Buy':
		if quote.latestPrice <= pendTrans.price1:
			buy(quote, pendTrans)

	elif pendTrans.transactionType == 'Limit Sell':
		if quote.latestPrice >= pendTrans.price1:
			sell(quote,pendTrans)

	return