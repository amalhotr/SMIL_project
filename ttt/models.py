from django.db import models

# Create your models here.
class League(models.Model):
    leagueName = models.CharField(max_length = 32)
    startingBalance = models.DecimalField(max_digits = 6 , decimal_places = 2)
    startDate = models.CharField(max_length = 10)
    endDate = models.CharField(max_length = 10)
    maxPlayers = models.IntegerField(default = 15)

class Transactions(models.Model):
    #username = models.ForeignKey('ttt.Player' , on_delete = models.CASCADE,)
    LeagueID = models.ForeignKey('ttt.League' , on_delete = models.CASCADE,)
    TransactionString = models.CharField(max_length = 100)

class PendingTransaction(models.Model):
    #username = models.ForeignKey('ttt.Player' , on_delete = models.CASCADE,)
    LeagueID = models.ForeignKey('ttt.League' , on_delete = models.CASCADE,)
    
    
