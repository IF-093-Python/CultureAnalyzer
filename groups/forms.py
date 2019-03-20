from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

from groups.models import Group, Shedule, Invitation
from groups.validators import dates_validator
from quiz.models import Quizzes

__all__ = ['GroupCreateForm', 'GroupUpdateForm', 'SheduleForm',
           'InvitationForm']


class GroupCreateForm(forms.ModelForm):
    """
    Creates group and adds mentors to it
    """

    class Meta:
        model = Group
        fields = ['name', 'mentor']
        widgets = {'mentor': forms.CheckboxSelectMultiple(), }


class GroupUpdateForm(forms.ModelForm):
    """
    Updates group by changing users in group
    """

    class Meta:
        model = Group
        fields = ['user']
        widgets = {'user': forms.CheckboxSelectMultiple(), }


class SheduleForm(forms.ModelForm):
    """
    Adds shedule to group
    """

    def __init__(self, *args, **kwargs):
        super(SheduleForm, self).__init__(*args, **kwargs)
        quizzes = Quizzes.objects.order_by('type_of_quiz', 'title')
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quizzes,
                                                     initial=quizzes.first())

    def clean(self):
        """Checking validity of dates"""
        cleaned_data = super(SheduleForm, self).clean()
        errors = dates_validator(data={
            'start': cleaned_data.get('begin'),
            'end': cleaned_data.get('end'),
            'form': 'SheduleForm', })
        for error in errors:
            self.add_error(error, errors[error])
        return cleaned_data

    class Meta:
        model = Shedule
        fields = ['begin', 'end', 'quiz']
        widgets = {
            'begin': DateTimePickerInput(options={'locale': 'en-gb', }),
            'end': DateTimePickerInput(options={'locale': 'en-gb', }),
        }


class InvitationForm(forms.ModelForm):
    """
    Makes URL by which users can join to group
    """

    def clean(self):
        """Checking validity of dates and number of students should be >0"""
        cleaned_data = super(InvitationForm, self).clean()
        errors = dates_validator(data={
            'start': cleaned_data.get('start'),
            'end': cleaned_data.get('end'),
            'items': cleaned_data.get('items_left'),
            'form': 'InvitationForm', })
        for error in errors:
            self.add_error(error, errors[error])
        return cleaned_data

    class Meta:
        model = Invitation
        fields = ['start', 'end', 'items_left', 'group', 'code']
        labels = {'items_left': 'Number of students:'}
        widgets = {
            'start': DateTimePickerInput(options={'locale': 'en-gb', }),
            'end': DateTimePickerInput(options={'locale': 'en-gb', }),
        }
