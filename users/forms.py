from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group

from .choices import GENDER_CHOICES, EDUCATION_CHOICES
from .models import CustomUser
from .validators import ProfileValidator, PValidationError

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
        model = CustomUser
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    experience = forms.IntegerField(label='Experience in years')
    date_of_birth = forms.DateField(widget=DateInput())
    education = forms.ChoiceField(choices=EDUCATION_CHOICES_EMPTY_LABEL)
    gender = forms.ChoiceField(choices=GENDER_CHOICES_EMPTY_LABEL)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'image', 'experience',
                  'date_of_birth', 'education', 'gender']

    def clean_experience(self):
        try:
            return ProfileValidator.validate(self.cleaned_data)
        except PValidationError as err:
            self.add_error('experience', str(err))


class BlockUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['is_active', 'is_staff', 'groups']


class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].widget.attrs.update(size='10')

    class Meta:
        model = Group
        fields = ['name', 'permissions']
