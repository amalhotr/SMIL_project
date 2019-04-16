from django import forms

class QuoteForm(forms.Form):
	'''
	Class sets up ticker selection form
	'''
	ticker = forms.CharField(max_length=5, help_text='Enter the ticker')

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Asset, TransactionType, TimeInForce, League

class TradeForm(forms.Form):
	'''
	Class sets up the form required for buying and selling stocks.
	'''

	League_name = forms.ModelChoiceField(queryset=League.objects.none())

	def __init__(self, *args, **kwargs):
		'''
		Initializes the form and fields for arguments
		:param args: sends a non keyworded variable of unknown length to the form
		:param kwargs: sends a keyworded variable of unknown length to the form
		'''
		user = kwargs.pop('user')
		super(TradeForm, self).__init__(*args, **kwargs)
		qs = League.objects.filter(players=user)
		self.fields['League_name'].queryset = qs
	asset = forms.ModelChoiceField(queryset=Asset.objects)
	transactionType = forms.ModelChoiceField(queryset=TransactionType.objects)
	timeInForce = forms.ModelChoiceField(queryset=TimeInForce.objects)
	price1 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, help_text='Enter the price for this transaction')
	price2 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, help_text='Enter the price for this transaction')
	quantity = forms.IntegerField(validators=[MinValueValidator(1)], help_text='Enter the quantity for this transaction')

class LeagueForm(forms.Form):
	'''
	Class set up for searching and creating leagues.
	Displays all existing League Object Models.
	'''
	League_name = forms.ModelChoiceField(queryset=League.objects.none())

	def __init__(self, *args, **kwargs):
		'''
		initializes the form and fields for arguments
		:param args: sends a non keyworded variable of unknown length to the form
		:param kwargs: sends a keyworded variable of unknown length to the form
		'''
		user = kwargs.pop('user')
		super(LeagueForm, self).__init__(*args, **kwargs)
		qs = League.objects.filter(players=user)
		self.fields['League_name'].queryset = qs

from django.forms import ModelForm

class AdminLeagueForm(ModelForm):
	'''
	Class the creates the form for making new leagues from the admin side
	and setting their attributes.
	'''
	class Meta:
		'''
		sets up the forms for league creation by an admin
		:param model: Creates the new league model to be added to the database
		'''
		model = League
		fields= ['startingBalance', 'startDate', 'endDate', 'public', 'description']

class CreateLeagueForm(ModelForm):
	'''
	Class the creates the form for making new leagues from the user side
	and setting their attributes.
	'''
	class Meta:
		'''
		sets up the forms for league creation by a user
		:param model: Creates the new league model to be added to the database
		'''
		model = League
		fields = ['name', 'startingBalance', 'startDate', 'endDate', 'public', 'description']