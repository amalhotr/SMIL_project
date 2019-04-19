from django.urls import path, include

from . import views
from machina import urls as machina_urls

urlpatterns = [
    path('', views.home, name='home'),
    path('trade/', views.trade, name='trade'),
    path('trade/ticker/<str:asset>/<str:ticker>', views.ticker, name='ticker'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:league>', views.dashboardLeague, name='ticker'),
    path('leagues/', views.leagues, name='leagues'),
    path('leagues/create', views.createLeague, name='createLeague'),
    path('leagues/admin/<str:leagueName>', views.adminLeague, name="adminLeague"),
    path('leagues/leave/<str:leagueName>', views.leaveLeague, name='leaveLeague'),
    path('leagues/join/<str:leagueName>', views.joinLeague, name='joinLeague'),
    path('forum/', include(machina_urls), name='forum'),
<<<<<<< HEAD
    path('/dashboard/export_csv/<str:portfolio_id>', views.exportCSV, name='exportCSV'),
=======
    path('dashboard/export/csv/<str:portfolio_id>', views.export_users_csv, name='export_users_csv'),
>>>>>>> 102115208a192ca614a1eb91030ba8e800b0c5d0
]
