from django.shortcuts import render
from django.http import HttpResponse
from .StockData import *
from .Plot import *

from django.views.generic import TemplateView

'''
import plotly.offline as opy
import plotly.graph_objs as go
'''

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        x,y = StockData.getValues('BTC', currency='crypto')
        context['graph']=Plot.getLinePlot(x,y, 'test')
        return context

class TradePageView(TemplateView):
    template_name = 'trade.html'

class DashboardPageView(TemplateView):
    template_name = 'dashboard.html'

