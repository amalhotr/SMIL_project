from django import forms
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper

class QuoteForm(forms.Form):
	'''
	Class sets up ticker selection form
	'''
	ticker = forms.CharField(
                                widget=forms.TextInput(attrs={'placeholder':'Enter Here'})
                                 )
	def __init__(self, *args, **kwargs):
                super().__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.layout = Layout(
                        Row(
                        Column('ticker' , css_class='form-group col-md-6 mb-0'),
                        css_class = 'form-row'
                        ),
                        Submit('submit','Submit',css_class='btn-secondary')
                        )

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Asset, TransactionType, TimeInForce, League

class TradeForm(forms.Form):
	'''
	Class sets up the form required for buying and selling stocks.
	'''

	League_name = forms.ModelChoiceField(queryset=League.objects)

	asset = forms.ModelChoiceField(queryset=Asset.objects)
	transactionType = forms.ModelChoiceField(queryset=TransactionType.objects)
	timeInForce = forms.ModelChoiceField(queryset=TimeInForce.objects)
	price1 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Price'}))
	price2 = forms.DecimalField(max_digits=11, decimal_places=2, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Price'}))
	quantity = forms.IntegerField(validators=[MinValueValidator(1)], widget=forms.TextInput(attrs={'placeholder':'Enter Quantity'}))

	

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
		super().__init__(*args,**kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
                        Row(
                                Column('League_name', css_class='form-group col-xl-6 mb-0'),
                                Column('asset' , css_class='form-group col-xl-6 mb-0'),
                                Column('transactionType' , css_class='form-group col-xl-6 mb-0'),
                                Column('timeInForce' , css_class='form-group col-xl-6 mb-0'),
                                css_class = 'form-row'
                        ),
                        Row(
                                Column('price1', css_class='form-group col-xl-6 mb-0'),
                                Column('price2' , css_class='form-group col-xl-6 mb-0'),
                                Column('quantity' , css_class='form-group col-xl-6 mb-0'),
                                css_class = 'form-row'
                                
                        ),
                        Submit('submit','Submit')
                )


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
