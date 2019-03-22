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
from .forms import QuoteForm, TradeForm, LeagueForm, CreateLeagueForm

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        x,y = StockData.getValues('BTC', currency='crypto')
        context['graph']=Plot.getLinePlot(x,y, 'test')
        return context

def trade(request):
	"""View function for home page of site."""
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			ticker = form.cleaned_data['ticker']
			return HttpResponseRedirect('ticker/' + ticker)
			
	else:
		form = QuoteForm()

	return render(request, 'index.html', {'form': form})

import uuid
from datetime import datetime

from .iex import getQuote, getKeyStats

@login_required
def ticker(request, ticker):
	quote = getQuote(ticker)
	keyStats = getKeyStats(ticker)
	if request.method == 'POST':
		form = TradeForm(request.POST, user=request.user)
		if form.is_valid():
			instance = PendingTransaction(id=uuid.uuid4(), player = request.user, league= form.cleaned_data['League_name'], asset = form.cleaned_data['asset'], ticker = ticker, transactionType = form.cleaned_data['transactionType'], timeInForce = form.cleaned_data['timeInForce'], transactionStatus = 'q', submittedDateTime = datetime.now(), price1 = form.cleaned_data['price1'], price2 = form.cleaned_data['price2'], quantity = form.cleaned_data['quantity'])
			instance.save()
			return HttpResponseRedirect('/dashboard/' + str(instance.league))
	else:
		form = TradeForm(user=request.user)

	context = {
		'ticker': ticker,
		'quote': quote,
		'keyStats': keyStats,
		'form': form
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
	return render(request, 'dashboardLeague.html', context)

@login_required
def leagues(request):
	"""View function for leagues page of site."""
	leag = League.objects.filter(public=True)

	context = {
		'leagues': leag,
	}
	return render(request, 'leagues.html', context)

@login_required
def joinLeague(request, leagueName):
	leagueName = unquote(leagueName)
	league = League.objects.get(name = leagueName)
	league.players.add(request.user)
	return HttpResponseRedirect('/')


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

