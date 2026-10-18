# app/user_info/forms.py

from django import forms 
from django_quill.forms       import QuillFormField
from django.core.validators   import URLValidator
import datetime

class UserProfileForm(forms.Form):
	profile_username = forms.CharField(
		label="Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class' : 'bnd-input bnd-border'}),
		)
	profile_password_1 = forms.CharField(
		label="Password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'bnd-input bnd-border'}),
		)
	profile_password_2 = forms.CharField(
		label="Password (reconfirm)", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'bnd-input bnd-border'}),
		)
	profile_email = forms.CharField(
		label="e-mail address", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'bnd-input bnd-border', 
								      'autocomplete' : 'email'}),
		)
	profile_first_name = forms.CharField(
		label="First Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'bnd-input bnd-border', 
								      'autocomplete' : 'given-name'}),
		)
	profile_last_name = forms.CharField(
		label="Last Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'bnd-input bnd-border', 
								      'autocomplete' : 'family-name'}),
		)
	profile_photo = forms.ImageField(
		required=False,
		widget=forms.FileInput()
	)
	
class UserLoginForm(forms.Form):
	username = forms.CharField(
		label="Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'bnd-input bnd-border'}),
		)
	password = forms.CharField(
		label="Password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class': 'bnd-input bnd-border'}),
		)
	
class UserPwdResetForm(forms.Form):
	
	pwd_rst_password_1 = forms.CharField(
		label="New Password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'bnd-input bnd-border'}),
		)
	pwd_rst_password_2 = forms.CharField(
		label="New Password (confirm)", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'bnd-input bnd-border'}),
		)
	pwd_rst_email = forms.CharField(
		label="Enter your e-mail address", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'bnd-input bnd-border', 
								      'autocomplete' : 'email'}),
		)

class EmailVerificationForm(forms.Form):
	entered_code = forms.CharField(
		label="Code:",
		max_length=16, 
		required=True,
		)