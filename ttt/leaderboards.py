from .models import *
from django.shortcuts import render
from .StockData import *
from .Plot import *
import operator
from .iex import *


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



def leaderboards(request):
    position = {}
    playerLeagues = Portfolio.objects.filter(league=request)
    for i in playerLeagues:
        position[i.player]= i.cash
        playersHolding = Holding.objects.filter(portfolio=i.id)
        for j in playersHolding:
            price = int(getQuote(j.ticker)["latestPrice"])
            total = price * j.quantity
            position[i.player] += total

    #sorted_p = sorted(position.items(), key=lambda x: x[1])
    return position

