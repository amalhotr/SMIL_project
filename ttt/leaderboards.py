from .models import *
import collections
import operator
from .iex import *

'''
import plotly.offline as opy
import plotly.graph_objs as go
'''

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

    position = collections.OrderedDict(sorted(position.items(), key=operator.itemgetter(1)))
    position = collections.OrderedDict(reversed(position.items()))

    return position

