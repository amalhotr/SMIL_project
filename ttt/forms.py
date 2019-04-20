from django import forms
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper
from .models import Asset, TransactionType, TimeInForce, League

class QuoteForm(forms.Form):
	'''
	Class sets up ticker selection form
	'''
	ticker = forms.CharField(max_length=8, help_text='Enter the ticker', widget=forms.TextInput(attrs={'class': 'form-control'}))
	asset = forms.ModelChoiceField(queryset=Asset.objects, widget=forms.Select(attrs={'class': 'form-control'}))

from django.core.validators import MinValueValidator, MaxValueValidator



class TradeForm(forms.Form):
	'''
	Class sets up the form required for buying and selling stocks.
	'''

	League_name = forms.ModelChoiceField(queryset=League.objects.none(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

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
	transactionType = forms.ModelChoiceField(queryset=TransactionType.objects, empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
	timeInForce = forms.ModelChoiceField(queryset=TimeInForce.objects, empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
	price1 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, help_text='Enter the price for this transaction', widget=forms.NumberInput(attrs={'class': 'form-control'}))
	price2 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, help_text='Enter the price for this transaction',  widget=forms.NumberInput(attrs={'class': 'form-control'}))
	quantity = forms.IntegerField(validators=[MinValueValidator(1)], help_text='Enter the quantity for this transaction',  widget=forms.NumberInput(attrs={'class': 'form-control'}))

class LeagueForm(forms.Form):
	'''
	Class set up for searching and creating leagues.
	Displays all existing League Object Models.
	'''
	League_name = forms.ModelChoiceField(queryset=League.objects.none(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

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
		labels = {
			"players": "Remove player(s)",
		}
		fields= ['players', 'startingBalance', 'startDate', 'endDate', 'public', 'description']

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
