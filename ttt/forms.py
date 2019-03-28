from django import forms

class QuoteForm(forms.Form):
	ticker = forms.CharField(max_length=5, help_text='Enter the ticker')

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Asset, TransactionType, TimeInForce, League

class TradeForm(forms.Form):
	League_name = forms.ModelChoiceField(queryset=League.objects.none())

	def __init__(self, *args, **kwargs):
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
	League_name = forms.ModelChoiceField(queryset=League.objects.none())

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(LeagueForm, self).__init__(*args, **kwargs)
		qs = League.objects.filter(players=user)
		self.fields['League_name'].queryset = qs

from django.forms import ModelForm

class AdminLeagueForm(ModelForm):
	class Meta:
		model = League
		fields= ['startingBalance', 'startDate', 'endDate', 'public', 'description']

class CreateLeagueForm(ModelForm):
	class Meta:
		model = League
		fields = ['name', 'startingBalance', 'startDate', 'endDate', 'public', 'description']