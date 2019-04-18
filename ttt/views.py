from django.shortcuts import render
from .StockData import *
from .Plot import *

from django.views.generic import TemplateView

'''
import plotly.offline as opy
import plotly.graph_objs as go
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction, Portfolio, Holding
from .forms import QuoteForm, TradeForm, LeagueForm, AdminLeagueForm, CreateLeagueForm

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

	quote = getQuote(tickerIEX)
	keyStats = getKeyStats(tickerIEX)
	news = getNews(tickerIEX)
	if request.method == 'POST':
		form = TradeForm(request.POST, user=request.user)
		if form.is_valid():
			instance = PendingTransaction(id=uuid.uuid4(), player = request.user, league= form.cleaned_data['League_name'], asset = form.cleaned_data['asset'], ticker = ticker, transactionType = form.cleaned_data['transactionType'], timeInForce = form.cleaned_data['timeInForce'], transactionStatus = 'q', submittedDateTime = datetime.now(), price1 = form.cleaned_data['price1'], price2 = form.cleaned_data['price2'], quantity = form.cleaned_data['quantity'])
			instance.save()
			return HttpResponseRedirect('/dashboard/' + str(instance.league))
	else:
		form = TradeForm(user=request.user)

	dates, values = StockData.getValues(ticker, asset)
	div = Plot.getLinePlot(dates, values, ticker)

	pred_dates, pred_values = StockData.getForecast(dates, values)
	prediction_div = Plot.getTwoPlots(dates, values, pred_dates, pred_values, ticker)
	context = {
		'ticker': ticker,
		'quote': quote,
		'news': news,
		'keyStats': keyStats,
		'form': form,
		'plot': div,
		'prediction_plot': prediction_div
	}
	return render(request, 'ticker.html', context)

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

	if request.method == 'POST':
		form = LeagueForm(request.POST, user=request.user)
		if form.is_valid():
			league = form.cleaned_data['League_name']
			return HttpResponseRedirect('/dashboard/' + str(league))
	else:
		form = LeagueForm(user=request.user, initial={'League_name': league})

	pendingTransactions = PendingTransaction.objects.filter(player=request.user, league=league)
	transactionHistory = TransactionHistory.objects.filter(player=request.user, league=league)
	portfolio = Portfolio.objects.filter(player=request.user, league=league)

	if len(portfolio)>0:
		holding = Holding.objects.filter(portfolio=portfolio[0])
		tickers = []
		quantities = []

		for hold in holding.iterator():
			tickers.append(hold.ticker)
			quantities.append(hold.quantity)

		pie_chart_div = Plot.getPieChart(tickers, quantities, 'Holdings')
	else:
		holding = None
		pie_chart_div = None




	context = {
		'form': form,
		'league': league,
		'pendingTransactions': pendingTransactions,
		'transactionHistory': transactionHistory,
		'holding':holding,
		'pie_chart':pie_chart_div,
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
