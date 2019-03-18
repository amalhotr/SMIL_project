from django.contrib import admin

from .models import League
from .models import Transactions

admin.site.register(League)
admin.site.register(Transactions)
