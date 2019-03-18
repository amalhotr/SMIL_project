from django.shortcuts import render
from django.http import HttpResponse
from .StockData import *

from django.views.generic import TemplateView

import plotly.offline as opy
import plotly.graph_objs as go

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        x,y = StockData.getValues()
        trace1 = go.Scatter(x=x,y=y, marker={'color':'red', 'symbol':'circle', 'size':10},mode='lines', name='1st trace')

        data=go.Data([trace1])
        layout=go.Layout(title='MSFT',xaxis={'title':'Date'}, yaxis={'title':'Value'})
        figure=go.Figure(data=data, layout=layout)
        div=opy.plot(figure, auto_open=False, output_type='div')

        context['graph']=div
        return context

class TradePageView(TemplateView):
    template_name = 'trade.html'

class DashboardPageView(TemplateView):
    template_name = 'dashboard.html'

