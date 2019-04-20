from django.shortcuts import render
from .StockData import *
from .Plot import *
from .leaderboards import *

from django.views.generic import TemplateView

'''
import plotly.offline as opy
import plotly.graph_objs as go
'''

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction, Portfolio, Holding
from .forms import QuoteForm, TradeForm, LeagueForm, AdminLeagueForm, CreateLeagueForm

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import csv

def home(request):
	'''
	Sends user to home page
	:param request: 'Home'
	:return: Renders the homepage
	'''
	return render(request, "home.html")

def trade(request):
	'''
	Sends user to trade page
	:param request: 'Trade'
	:return: Renders the Trade Page
	'''
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			ticker = form.cleaned_data['ticker']
			asset = form.cleaned_data['asset']
			return HttpResponseRedirect('ticker/' + str(asset) + '/' + ticker)

	else:
		form = QuoteForm()

	return render(request, 'trade.html', {'form': form})

import uuid
from datetime import datetime

from .iex import getQuote, getKeyStats, getNews

@login_required
def ticker(request, asset, ticker):
	'''
	Receive information about given stock and enter settings to buy and sell.
	:param request: 'Ticker'
	:param ticker: string of the ticker for corresponding stock
	:return: Renders a page with information about stock corresponding to ticker given
	'''
	if asset == 'Cryptocurrency':
		tickerIEX = ticker + 'USDT'
	else:
		tickerIEX = ticker

	try:
		quote = getQuote(tickerIEX)
	except Exception:
		messages.info(request, 'You have entered an invalid ticker or selected the wrong type of asset. PLEASE TRY AGAIN!')
		return HttpResponseRedirect('/trade/')

	keyStats = getKeyStats(tickerIEX)
	news = getNews(tickerIEX)
	if request.method == 'POST':
		quoteForm = QuoteForm(request.POST)
		tradeForm = TradeForm(request.POST, user=request.user)
		if quoteForm.is_valid():
			ticker = quoteForm.cleaned_data['ticker']
			asset = quoteForm.cleaned_data['asset']
			return HttpResponseRedirect('/trade/ticker/' + str(asset) + '/' + ticker)
		elif tradeForm.is_valid():
			instance = PendingTransaction(id=uuid.uuid4(), player = request.user, league= tradeForm.cleaned_data['League_name'], asset = Asset.objects.get(name=asset), ticker = ticker, transactionType = tradeForm.cleaned_data['transactionType'], timeInForce = tradeForm.cleaned_data['timeInForce'], transactionStatus = 'q', submittedDateTime = datetime.now(), price1 = tradeForm.cleaned_data['price1'], price2 = tradeForm.cleaned_data['price2'], quantity = tradeForm.cleaned_data['quantity'])
			instance.save()
			return HttpResponseRedirect('/dashboard/' + str(instance.league))
	else:
		quoteForm = QuoteForm()
		tradeForm = TradeForm(user=request.user)

	dates, values = StockData.getValues(ticker, asset)
	div = Plot.getLinePlot(dates, values, ticker)

	context = {
		'ticker': ticker,
		'asset': asset,
		'quote': quote,
		'news': news,
		'keyStats': keyStats,
		'quoteForm': quoteForm,
		'tradeForm': tradeForm,
		'plot': div,
	}
	return render(request, 'ticker.html', context)

@login_required
def deleteTrans(request, transId):
	try:
		pendTrans = PendingTransaction.objects.get(id=transId)
		league = pendTrans.league
		pendTrans.delete()
		return HttpResponseRedirect('/dashboard/' + league.name)
	except:
		return HttpResponseRedirect('/dashboard/')

@login_required
def dashboard(request):
	'''
	Sends user to the dashboard
	:param request: 'Dashboard'
	:return: Renders the user's dashboard
	'''
	if request.method == 'POST':
		form = LeagueForm(request.POST, user=request.user)
		if form.is_valid():
			league = form.cleaned_data['League_name']
			return HttpResponseRedirect(str(league))
	else:
		form = LeagueForm(user=request.user)
	return render(request, 'dashboard.html', {'form': form})

from urllib.parse import unquote

@login_required
def dashboardLeague(request, league):
	'''
	Sends the user to the league's dashboard
	:param request: 'League dashboard'
	:param league: League name of the requested dashboard
	:return: Renders the league's dashboard
	'''
	league = unquote(league)
	leagueObject = League.objects.get(name=league)
	if request.method == 'POST':
		form = LeagueForm(request.POST, user=request.user)
		if form.is_valid():
			league = form.cleaned_data['League_name']
			return HttpResponseRedirect('/dashboard/' + str(league))
	else:
		form = LeagueForm(user=request.user, initial={'League_name': league})

	pendingTransactions = PendingTransaction.objects.filter(player=request.user, league=league).order_by('-submittedDateTime')
	transactionHistory = TransactionHistory.objects.filter(player=request.user, league=league).order_by('-fulfilledDateTime')
	position = leaderboards(league)

	try:
		portfolio = Portfolio.objects.get(player=request.user, league=leagueObject)
	except:
		portfolio = Portfolio(id=uuid.uuid4(), player=request.user, league=leagueObject, cash=leagueObject.startingBalance)

	portfolio_id = portfolio.id

	totVal = portfolio.cash
	playersHolding = Holding.objects.filter(portfolio=portfolio_id)
	for j in playersHolding:
		try:
			price = int(getQuote(j.ticker)["latestPrice"])
		except Exception:
			app = 'USDT'
			ticker = j.ticker + app
			price = int(getQuote(ticker)["latestPrice"])
		total = price * j.quantity
		totVal += total

	if portfolio:
		holding = Holding.objects.filter(portfolio=portfolio).order_by('ticker', '-quantity')
		tickers = []
		prices = []

		for hold in holding.iterator():
			tickers.append(hold.ticker)
			prices.append(hold.price)

		pie_chart_div = Plot.getPieChart(tickers, prices, 'Holdings')
	else:
		holding = None
		pie_chart_div = None
		portfolio_id = None

	context = {
		'form': form,
		'league': league,
		'pendingTransactions': pendingTransactions,
		'transactionHistory': transactionHistory,
		'holding':holding,
		'portfolio': portfolio,
        'position':position,
		'pie_chart':pie_chart_div,
		'portfolio_id':portfolio_id,
		'totVal':totVal,
	}
	return render(request, 'dashBoardLeague.html', context)

@login_required
def leagues(request):
	'''
	Sends user to the page with the list of leagues
	:param request: 'Leagues'
	:return: Renders the page of Leagues
	'''
	adminLeagues = League.objects.filter(admin=request.user)
	playerLeagues = League.objects.filter(players=request.user).exclude(admin=request.user)
	publicLeagues = League.objects.filter(public=True)

	context = {
		'adminLeagues': adminLeagues,
		'playerLeagues': playerLeagues,
		'publicLeagues': publicLeagues,

	}
	return render(request, 'leagues.html', context)

@login_required
def createLeague(request):
	'''
	Sends the user to a page to create a league
	:param request: 'Create league'
	:return: Renders the page and settings for the user to create a league
	'''
	if request.method == 'POST':
		form = CreateLeagueForm(request.POST)
		if form.is_valid():
			instance = League(admin = request.user, name = form.cleaned_data['name'], startingBalance = form.cleaned_data['startingBalance'], startDate = form.cleaned_data['startDate'], endDate = form.cleaned_data['endDate'], public = form.cleaned_data['public'], description = form.cleaned_data['description'])
			# instance.players.add(request.user)
			instance.save()
			instance.players.add(request.user)
			return HttpResponseRedirect('/leagues/')
	else:
		form = CreateLeagueForm()
	return render(request, 'createLeague.html', {'form': form})

@login_required
def adminLeague(request, leagueName):
	'''
	Sends the user to a page to create an administrative league
	:param request: 'Admin league'
	:param leagueName: Name of the league requested
	:return: Renders the page to the administrative league creation
	'''
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	if request.method == 'POST':
		form = AdminLeagueForm(request.POST)
		if form.is_valid():
			removedPlayers = form.cleaned_data['players']
			league.players.remove(*removedPlayers);
			league.startingBalance = form.cleaned_data['startingBalance']
			league.startDate = form.cleaned_data['startDate']
			league.endDate = form.cleaned_data['endDate']
			league.public = form.cleaned_data['public']
			league.description = form.cleaned_data['description']
			league.save()
			return HttpResponseRedirect('/leagues/')
	else:
		form = AdminLeagueForm(initial={'startingBalance': league.startingBalance, 'startDate': league.startDate, 'endDate': league.endDate, 'public': league.public, 'description': league.description})
		form.fields['players'].queryset = league.players;
	context = {
		'leagueName': leagueName,
		'form': form
	}
	return render(request, 'adminLeague.html', context)

@login_required
def leaveLeague(request, leagueName):
	'''
	Deletes user's information from the requested league's database
	:param request: 'Leave league'
	:param leagueName: Name of league user wants to leave
	:return: Removes the user from the league
	'''
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	league.players.remove(request.user)
	return HttpResponseRedirect('/leagues/')

@login_required
def joinLeague(request, leagueName):
	'''
	Adds the user to the requested league's database
	:param request: 'Join league'
	:param leagueName: Name of league user wants to join
	:return: Adds user to the league
	'''
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	league.players.add(request.user)
	return HttpResponseRedirect('/leagues/')

@login_required
def exportCSV(request, portfolio_id):
	'''
	Export users holding data to CSV file
	:param request: 'Join league'
	:param portfolio_id: id of portfolio
	:return: Http response with file download
	'''
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename = "test.csv"'

	writer = csv.writer(response)
	writer.writerow(['Ticker', 'Quantity', 'Price'])

	portfolio = Portfolio.objects.filter(id=portfolio_id)
	if len(portfolio)>0:
		holding = Holding.objects.filter(portfolio=portfolio[0])

		for hold in holding.iterator():
			writer.writerow([hold.ticker, hold.quantity, hold.price])

	return response

@login_required
def predictionTab(request, asset, ticker, accuracy):
	'''
	Open new tab with prediction for a specific stock
	:param asset: type of asset (stock or crypto)
	:param ticker: ticker of given stock or crypto
	:param accuracy: a level of accuracy for the forecast
	:return: renders page with plot showing forecast
	'''
	dates, values = StockData.getValues(ticker, asset)

	if int(accuracy)>1 and int(accuracy)<200:
		pred_dates, pred_values = StockData.getForecast(dates, values, seasonal_period=int(accuracy))
		prediction_div = Plot.getTwoPlots(dates, values, pred_dates, pred_values, ticker)
	else:
		pred_dates, pred_values = StockData.getForecast(dates, values)
		prediction_div = Plot.getTwoPlots(dates, values, pred_dates, pred_values, ticker)

	context = {
		'prediction_plot':prediction_div,
	}
	return render(request, 'prediction.html', context)
