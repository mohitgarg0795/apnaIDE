
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
		fields=('username','email','password')		#tuple of fields to be included in the form
	
	def clean(self):		#performs cross field/multiple fields validation
		if self.cleaned_data.get('password')!=self.cleaned_data.get('repassword'):
			raise forms.ValidationError("Passwords do not match.")
		return self.cleaned_data		#this is the final cleaned_data that is processed further, u can return any values here as u wish

	def clean_username(self):
		new_user=self.cleaned_data['username']
		if User.objects.all().filter(username=new_user).exists():
			raise forms.ValidationError("This username already exists, please choose another one")
		return new_user

	def clean_email(self):
		mail_id=self.cleaned_data['email']
		if User.objects.all().filter(email=mail_id).exists():
			raise forms.ValidationError("This email id already exists, please use another one")
		return mail_id