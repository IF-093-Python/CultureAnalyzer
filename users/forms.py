from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=40, label='', widget=forms.TextInput(
        attrs={
            'class': 'input_attr',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input_attr',
            'placeholder': 'Password'
        }
    ), label='')

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


