from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField

class RegisterForm(UserCreationForm):
	password1 = forms.CharField(
		widget= forms.PasswordInput(attrs={'label':'','type':'password', 'align':'center', 'placeholder':'Password'})
		)
	password2 = forms.CharField(
		widget= forms.PasswordInput(attrs={'id':'user', 'type':'password', 'align':'center', 'placeholder':'Confirm Password'}))
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		widgets = {
            'username': forms.TextInput(attrs={'id' :'user', 'label':'','align':'center','placeholder':'Username'}), 		
        }
		
	def __init__(self, *args, **kwargs):
			super(RegisterForm, self).__init__(*args, **kwargs)

			for fieldname in ['username', 'password1', 'password2']:
				self.fields[fieldname].help_text = None
				self.fields[fieldname].label = ''
				
class LoginForm(AuthenticationForm):
    username = UsernameField(label='Enter Username', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))