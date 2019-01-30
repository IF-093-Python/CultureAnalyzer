from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from .validators import ProfileValidator
from .choices import GENDER_CHOICES, EDUCATION_CHOICES


# this form we use to show normal calendar in template
class DateInput(forms.DateInput):
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
    age = forms.DateField(widget=DateInput())
    education = forms.ChoiceField(choices=EDUCATION_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial='')

    class Meta:
        model = Profile
        fields = ['image', 'experience', 'age', 'education', 'gender']

    def clean_experience(self):
        return ProfileValidator.validate_experience(self.cleaned_data)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


