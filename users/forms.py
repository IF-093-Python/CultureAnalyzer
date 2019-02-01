from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .choices import GENDER_CHOICES, EDUCATION_CHOICES
from .models import Profile
from .validators import ProfileValidator

__all__ = [
    'UserLoginForm',
    'UserRegisterForm',
    'ProfileUpdateForm',
    'UserUpdateForm',
    'EDUCATION_CHOICES_EMPTY_LABEL',
    'GENDER_CHOICES_EMPTY_LABEL',
]

EDUCATION_CHOICES_EMPTY_LABEL = (('', '--------------'),) + EDUCATION_CHOICES
GENDER_CHOICES_EMPTY_LABEL = (('', '--------------'),) + GENDER_CHOICES


class DateInput(forms.DateInput):
    """this form we use to show normal calendar in template
    instead text field
    """
    input_type = 'date'


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


class ProfileUpdateForm(forms.ModelForm):
    experience = forms.IntegerField()
    date_of_birth = forms.DateField(widget=DateInput())
    education = forms.ChoiceField(choices=EDUCATION_CHOICES_EMPTY_LABEL)
    gender = forms.ChoiceField(choices=GENDER_CHOICES_EMPTY_LABEL)

    class Meta:
        model = Profile
        fields = ['image', 'experience', 'date_of_birth', 'education',
                  'gender']

    def clean_experience(self):
        return ProfileValidator.validate(self.cleaned_data)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
