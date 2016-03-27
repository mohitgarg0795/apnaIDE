from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


"""class RegisterForm(forms.Form):
	username=forms.CharField(max_length=50, label="Enter Username")
	email=forms.EmailField(label="Enter Email ID")
	password=forms.CharField(max_length=100,widget=forms.PasswordInput(),label="Enter Password")
	repassword=forms.CharField(max_length=100,widget=forms.PasswordInput(),label="Confirm Password")
"""

class UserForm(forms.ModelForm):
	username=forms.CharField(max_length=50, label="Enter Username")
	email=forms.EmailField(label="Enter Email ID")
	password=forms.CharField(max_length=100,widget=forms.PasswordInput())	#overrides the original password field of User coz that shows password entered
	repassword=forms.CharField(max_length=100,widget=forms.PasswordInput(),label="Confirm Password")
	captcha=CaptchaField()

	class Meta:
		model=User
		fields=('username','email','password')
	
	def clean(self):
		if self.cleaned_data.get('password')!=self.cleaned_data.get('repassword'):
			raise forms.ValidationError("Passwords do not match.")
		return self.cleaned_data

	def clean_username(self):
		new_user=self.cleaned_data['username']
		if User.objects.all().filter(username=new_user):
			raise forms.ValidationError("This username already exists, please choose another one")
		return new_user