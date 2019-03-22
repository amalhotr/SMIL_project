from django.db import models
from django.contrib.auth.models import User
import uuid # Required for unique transaction instances

# Create your models here.
class League(models.Model):
	"""Model representing a league."""
	admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='league_admin')
	players = models.ManyToManyField(User, blank=True, related_name='league_players')
	name = models.CharField(max_length = 32, help_text='Enter a league name', primary_key=True)
	startingBalance = models.DecimalField(max_digits = 11, decimal_places = 2, help_text='Enter the starting balance of the league')
	startDate = models.DateField(help_text='Enter a starting date for the league')
	endDate = models.DateField(help_text='Enter a ending date for the league')
	public = models.BooleanField(default=True, help_text='Select true for public league.')
	description = models.TextField(max_length=1000, help_text='Enter a brief description of the league')

	class Meta:
		ordering = ['name']

	def __str__(self):
		"""String for representing the Model object"""
		return self.name

class Asset(models.Model):
	"""Model representing an asset."""
	name = models.CharField(max_length=100, help_text='Enter an asset (e.g. Crytocurrency)', primary_key=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		"""String for representing the Model object"""
		return self.name

class TransactionType(models.Model):
	"""Model representing a transaction type."""
	name = models.CharField(max_length=100, help_text='Enter a transaction type (e.g. Limit Sell)', primary_key=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		"""String for representing the Model object"""
		return self.name

class TimeInForce(models.Model):
	"""Model representing a time in force."""
	name = models.CharField(max_length=100, help_text='Enter a time in force (e.g. Good-til-canceled)', primary_key=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		"""String for representing the Model object"""
		return self.name

from django.core.validators import MinValueValidator, MaxValueValidator

class Holdings(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this transaction')
        ticker = models.CharField(max_length=5, help_text='Enter the ticker for this transaction')
        quantity = models.IntegerField(validators=[MinValueValidator(1)], help_text='Enter the quantity for this transaction')        

        class Meta:
                ordering = ['id']
        def __str__(self):
                """String for representing the Model object"""
                return f'{self.ticker}({str(self.id)})'

class TransactionHistory(models.Model):
        """Model representing transaction history."""
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this transaction')
        player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        league = models.ForeignKey(League, help_text='Select a league for this transaction', on_delete=models.CASCADE)
        asset = models.ForeignKey(Asset, help_text='Select an asset for this transaction', on_delete=models.CASCADE)
        ticker = models.CharField(max_length=5, help_text='Enter the ticker for this transaction')
        transactionType = models.ForeignKey(TransactionType, help_text='Select a transaction type for this transaction', on_delete=models.CASCADE)
        timeInForce = models.ForeignKey(TimeInForce, help_text='Select a time in force for this transaction', on_delete=models.CASCADE)

        TRANSACTION_STATUS = (
                ('f', 'Fulfilled'),
                ('c', 'Canceled'),
                )
	
        transactionStatus = models.CharField(max_length=1, choices=TRANSACTION_STATUS, help_text='Transaction status')
        submittedDateTime = models.DateTimeField(help_text='Enter the submitted date & time for this transaction')
        fulfilledDateTime = models.DateTimeField(help_text='Enter the fulfilled date & time for this transaction')
        price1 = models.DecimalField(max_digits=11, decimal_places=2, help_text='Enter the price for this transaction')
        price2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text='Enter the triggering price for this transaction')
        quantity = models.IntegerField(validators=[MinValueValidator(1)], help_text='Enter the quantity for this transaction')
        total = models.DecimalField(max_digits=11, decimal_places=2, help_text='Enter the total price for this transaction')
        holdings = models.ForeignKey(Holdings, on_delete=models.SET_NULL, null = True)

        class Meta:
                ordering = ['id']

        def __str__(self):
                """String for representing the Model object"""
                return f'{str(self.id)}'


class PendingTransaction(models.Model):
	"""Model representing pending transactions."""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this transaction')
	player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	league = models.ForeignKey(League, help_text='Select a league for this transaction', on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, help_text='Select an asset for this transaction', on_delete=models.CASCADE)
	ticker = models.CharField(max_length=5, help_text='Enter the ticker for this transaction')
	transactionType = models.ForeignKey(TransactionType, help_text='Select a transaction type for this transaction', on_delete=models.CASCADE)
	timeInForce = models.ForeignKey(TimeInForce, help_text='Select a time in force for this transaction', on_delete=models.CASCADE)

	TRANSACTION_STATUS = (
		('q', 'Queued'),
		('p', 'Placed'),
	)

	transactionStatus = models.CharField(max_length=1, choices=TRANSACTION_STATUS, help_text='Transaction status')
	submittedDateTime = models.DateTimeField(help_text='Enter the submitted date & time for this transaction')
	price1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text='Enter the price for this transaction')
	price2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text='Enter the triggering price for this transaction')
	quantity = models.IntegerField(validators=[MinValueValidator(1)], help_text='Enter the quantity for this transaction')

	class Meta:
		ordering = ['id']

	def __str__(self):
		"""String for representing the Model object"""
		return f'{self.id}'

	
class Portfolio(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this transaction')
        player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        league = models.ForeignKey(League, help_text='Select a league for this transaction', on_delete=models.CASCADE)
        cash = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, help_text='Current amount for player')

        class Meta:
                ordering = ['player' , 'league']
        def __str__(self):
                return f'{self.player}({self.league})'



