from django.contrib.auth import login, authenticate
from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordResetForm
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .validators import makeup, no_profanity



	
class RegisterForm(UserCreationForm):
	email = forms.CharField(
		widget=forms.TextInput(attrs={'class' :'user','class':'form-control', 'label':'','align':'center','placeholder':'Email'}
		))
	username = forms.CharField(validators = [MinLengthValidator(5), MaxLengthValidator(15),makeup,no_profanity],
		widget=forms.TextInput(attrs={'class' :'user','class':'form-control','name':'userReg', 'label':'Username','align':'center','placeholder':'Username'}
		))
	password1 = forms.CharField(
		widget= forms.PasswordInput(attrs={'label':'','type':'password', 'class':'form-control','align':'center', 'placeholder':'Password'})
		)
	password2 = forms.CharField(
		widget= forms.PasswordInput(attrs={'class':'user', 'type':'password', 'class':'form-control','align':'center', 'placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ['email', 'username', 'password1', 'password2']
		widgets = {
            'username': forms.TextInput(attrs={'claas' :'user', 'label':'Username','align':'center','placeholder':'Username'}), 		
        }
		
	def __init__(self, *args, **kwargs):
			super(RegisterForm, self).__init__(*args, **kwargs)

			for fieldname in ['username', 'password1', 'password2', 'email']:
				self.fields[fieldname].help_text = None
				self.fields[fieldname].label = ''
				


class loginForm(AuthenticationForm):
    username = UsernameField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username','name':'nameLog'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	
class resetForm(forms.Form):
	email =  forms.CharField(label='Enter email', widget=forms.PasswordInput(attrs={'class':'form-control'}))
class points_form(forms.Form):
	points = forms.CharField(widget=forms.TextInput(attrs={'position': 'absolute','label':'','readonly': 'readonly','name':"points", 'class':"points", 'value':0}))
	def __init__(self, *args, **kwargs):
		super(points_form, self).__init__(*args, **kwargs)
		self.fields['points'].label = ""
	

	


class email_form(forms.Form):
	first = forms.CharField(max_length=15, label='', widget=forms.TextInput(attrs={'class':'form-control','class':'formtr','type':'text','placeholder':'First name','size': 500}))
	last = forms.CharField(max_length=15, label='', widget=forms.TextInput(attrs={'class':'form-control','class':'formtr','type':'text','placeholder':'Last name','size': 500}))
	address = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class':'form-control','class':'formtr','type':'text','placeholder':'Address(not saved)','size': 500}))
	email = forms.CharField(max_length=60, label='', widget=forms.TextInput(attrs={'class':'form-control','class':'formtr','type':'text','placeholder':'Email','size': 500}))
	



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'reset_email',
        'placeholder': 'Email',
        'type': 'email',
        'name': 'email',
		'size': 500,
        }))


class repForm(forms.Form):
	address = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Address','id':'cj','size': 500}))