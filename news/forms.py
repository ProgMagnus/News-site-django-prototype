from django import forms
from .models import News
from captcha.fields import CaptchaField
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm): 
	username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=10, help_text='10 chars max', widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'})) 
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

class NewsForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = News
		fields = ['title', 'content', 'photo', 'is_published', 'category']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
			'photo': forms.FileInput(attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control'}),
		}
		

	def clean_title(self):
		title = self.cleaned_data['title']
		if re.match(r'\d', title):
			raise ValidationError('The title should not begin with a number')
		return title

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
	captcha = CaptchaField()

