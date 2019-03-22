from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('This User Does Not Exist!')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This User Is Not Active')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label = 'Email Address')
    password = forms.CharField(widget = forms.PasswordInput, label = "Enter Password")
    first = forms.CharField(label = 'Enter First Name')
    last = forms.CharField(label = 'Enter Last Name')
    class Meta:
        model = User
        fields = [
            'username',
            'first',
            'last',
            'email',
            'password'
        ]
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email = email)
        if email_qs.exists():
            raise forms.ValidationError('This Email Is Already In Use')
        return super(UserRegisterForm, self).clean(*args, **kwargs)

            
