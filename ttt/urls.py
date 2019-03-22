from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:league>', views.dashboardLeague, name='ticker'),
    path('leagues/', views.leagues, name='leagues'),
    path('trade/', views.trade, name='trade'),
    path('trade/ticker/<str:ticker>', views.ticker, name='ticker'),
    path('leagues/create', views.createLeague, name='createLeague'),
    path('leagues/join/<str:leagueName>', views.joinLeague, name='joinLeague'),
    
]
