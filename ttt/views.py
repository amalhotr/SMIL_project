from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class TradePageView(TemplateView):
    template_name = 'trade.html'

class DashboardPageView(TemplateView):
    template_name = 'dashboard.html'

