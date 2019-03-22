from django.contrib import admin

# Register your models here.
from ttt.models import League, Asset, TransactionType, TimeInForce, TransactionHistory, PendingTransaction, Holdings, Portfolio

# admin.site.register(League)
class LeagueAdmin(admin.ModelAdmin):
	list_display = ('name', 'startingBalance', 'startDate', 'endDate', 'public')

admin.site.register(League, LeagueAdmin)

admin.site.register(Asset)
admin.site.register(TransactionType)
admin.site.register(TimeInForce)

# admin.site.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
	list_filter = ('league', 'submittedDateTime', 'fulfilledDateTime')

	list_display = ('id', 'league', 'ticker', 'transactionType', 'transactionStatus', 'submittedDateTime', 'fulfilledDateTime', 'price1', 'quantity')

	fieldsets = (
		(None, {
			'fields': ('id', 'player', 'league' , 'holdings')
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
 	list_display = ('id', 'league', 'ticker', 'transactionType', 'transactionStatus', 'submittedDateTime', 'price1', 'quantity')

 	list_filter = ('league', 'submittedDateTime')

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

admin.site.register(Holdings)
admin.site.register(Portfolio)
