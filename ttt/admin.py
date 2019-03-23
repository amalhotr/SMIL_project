from django.contrib import admin

# Register your models here.
from ttt.models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction, Holding, Portfolio

# admin.site.register(League)
class LeagueAdmin(admin.ModelAdmin):
	list_display = ('name', 'startingBalance', 'startDate', 'endDate', 'public')

admin.site.register(League, LeagueAdmin)

admin.site.register(Asset)
admin.site.register(TransactionType)
admin.site.register(TimeInForce)

# admin.site.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
	list_filter = ('league', 'player', 'submittedDateTime', 'fulfilledDateTime')

	list_display = ('id', 'league', 'player', 'ticker', 'transactionType', 'transactionStatus', 'submittedDateTime', 'fulfilledDateTime', 'price1', 'quantity')

	fieldsets = (
		(None, {
			'fields': ('id', 'player', 'league')
			}),
		('Order', {
			'fields': ('asset', 'ticker', 'transactionType', 'timeInForce', 'price1', 'price2', 'quantity')
			}),
		('Status', {
			'fields': ('transactionStatus', 'submittedDateTime', 'fulfilledDateTime', 'total')
			}),
		)

admin.site.register(TransactionHistory, TransactionHistoryAdmin)

# admin.site.register(PendingTransaction)
class PendingTransactionAdmin(admin.ModelAdmin):
 	list_display = ('id', 'league', 'player', 'ticker', 'transactionType', 'transactionStatus', 'submittedDateTime', 'price1', 'quantity')

 	list_filter = ('league', 'player', 'submittedDateTime')

 	fieldsets = (
		(None, {
			'fields': ('id', 'player', 'league')
			}),
		('Order', {
			'fields': ('asset', 'ticker', 'transactionType', 'timeInForce', 'price1', 'price2', 'quantity')
			}),
		('Status', {
			'fields': ('transactionStatus', 'submittedDateTime')
			}),
		)

admin.site.register(PendingTransaction, PendingTransactionAdmin)

class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('id', 'player', 'league', 'cash')

	list_filter = ('player', 'league')

admin.site.register(Portfolio, PortfolioAdmin)

class HoldingAdmin(admin.ModelAdmin):
	list_display = ('id', 'ticker', 'price', 'quantity', 'portfolio')

	list_filter = ('portfolio', 'ticker')

admin.site.register(Holding, HoldingAdmin)

