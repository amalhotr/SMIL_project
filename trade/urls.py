from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('leagues/', views.leagues, name='leagues'),
	path('ticker/<str:ticker>', views.ticker, name='ticker'),
	path('dashboard/<str:league>', views.dashboardLeague, name='ticker'),
	path('leagues/create', views.createLeague, name='createLeague'),
	path('leagues/join/<str:leagueName>', views.joinLeague, name='joinLeague'),
]