from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trade/', views.trade, name='trade'),
    path('trade/ticker/<str:ticker>', views.ticker, name='ticker'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:league>', views.dashboardLeague, name='ticker'),
    path('leagues/', views.leagues, name='leagues'),
    path('leagues/create', views.createLeague, name='createLeague'),
    path('leagues/admin/<str:leagueName>', views.adminLeague, name="adminLeague"),
    path('leagues/leave/<str:leagueName>', views.leaveLeague, name='leaveLeague'),
    path('leagues/join/<str:leagueName>', views.joinLeague, name='joinLeague'),   
]