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

from .models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction
from .forms import QuoteForm, TradeForm, LeagueForm, AdminLeagueForm, CreateLeagueForm

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, "home.html")

def trade(request):
	"""View function for home page of site."""
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			ticker = form.cleaned_data['ticker']
			return HttpResponseRedirect('ticker/' + ticker)

	else:
		form = QuoteForm()

	return render(request, 'trade.html', {'form': form})

import uuid
from datetime import datetime

from .iex import getQuote, getKeyStats, getNews

@login_required
def ticker(request, ticker):
	"""View information about given Stock before buying. Enter settings to buy/sell. """
	quote = getQuote(ticker)
	keyStats = getKeyStats(ticker)
	news = getNews(ticker)
	if request.method == 'POST':
		form = TradeForm(request.POST, user=request.user)
		if form.is_valid():
			instance = PendingTransaction(id=uuid.uuid4(), player = request.user, league= form.cleaned_data['League_name'], asset = form.cleaned_data['asset'], ticker = ticker, transactionType = form.cleaned_data['transactionType'], timeInForce = form.cleaned_data['timeInForce'], transactionStatus = 'q', submittedDateTime = datetime.now(), price1 = form.cleaned_data['price1'], price2 = form.cleaned_data['price2'], quantity = form.cleaned_data['quantity'])
			instance.save()
			return HttpResponseRedirect('/dashboard/' + str(instance.league))
	else:
		form = TradeForm(user=request.user)

	data, values = StockData.getValues(ticker)
	div = Plot.getLinePlot(data, values, ticker)
	context = {
		'ticker': ticker,
		'quote': quote,
		'news': news,
		'keyStats': keyStats,
		'form': form,
		'plot': div
	}
	return render(request, 'ticker.html', context)

@login_required
def dashboard(request):
	"""View function for dashboard page of site."""
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

	context = {
		'form': form,
		'league': league,
		'pendingTransactions': pendingTransactions,
		'transactionHistory': transactionHistory
	}
	return render(request, 'dashBoardLeague.html', context)

@login_required
def leagues(request):
	"""View function for leagues page of site."""
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
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	if request.method == 'POST':
		form = AdminLeagueForm(request.POST)
		if form.is_valid():
			league.startingBalance = form.cleaned_data['startingBalance']
			league.startDate = form.cleaned_data['startDate']
			league.endDate = form.cleaned_data['endDate']
			league.public = form.cleaned_data['public']
			league.description = form.cleaned_data['description']
			league.save()
			return HttpResponseRedirect('/leagues/')
	else:
		form = AdminLeagueForm(initial={'startingBalance': league.startingBalance, 'startDate': league.startDate, 'endDate': league.endDate, 'public': league.public, 'description': league.description})
	context = {
		'leagueName': leagueName,
		'form': form
	}
	return render(request, 'adminLeague.html', context)

@login_required
def leaveLeague(request, leagueName):
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	league.players.remove(request.user)
	return HttpResponseRedirect('/leagues/')
	
@login_required
def joinLeague(request, leagueName):
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	league.players.add(request.user)
	return HttpResponseRedirect('/leagues/')