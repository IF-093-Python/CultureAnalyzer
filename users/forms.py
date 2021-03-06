from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple

from CultureAnalyzer.exceptions import PValidationError
from users.choices import GENDER_CHOICES, EDUCATION_CHOICES
from users.validators import ProfileValidator

__all__ = [
    'UserLoginForm',
    'UserRegisterForm',
    'UserUpdateForm',
    'BlockUserForm',
    'GroupForm',
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
        model = get_user_model()
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    experience = forms.IntegerField()
    date_of_birth = forms.DateField(widget=DateInput())
    education = forms.ChoiceField(choices=EDUCATION_CHOICES_EMPTY_LABEL)
    gender = forms.ChoiceField(choices=GENDER_CHOICES_EMPTY_LABEL)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'image', 'experience',
                  'date_of_birth', 'education', 'gender']

    def clean_experience(self):
        try:
            return ProfileValidator.validate(
                self.cleaned_data.get('experience'))
        except PValidationError as err:
            self.add_error('experience', str(err))


class BlockUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget = CheckboxSelectMultiple()

    class Meta:
        model = get_user_model()
        fields = ['is_active', 'groups']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
