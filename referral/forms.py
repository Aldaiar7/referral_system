from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from user.models import User
    

class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email','referral_token', 'password1', 'password2')



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
