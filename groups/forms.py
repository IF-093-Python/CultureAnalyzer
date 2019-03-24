from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

from groups.models import Group, Shedule, Invitation
from groups.validators import InvitationValidator, SheduleValidator
from quiz.models import Quizzes
from CultureAnalyzer.exceptions import PValidationError

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

    def clean_start(self):
        """Checks validity of start date"""
        start = self.cleaned_data.get('start')
        try:
            return SheduleValidator.start_validator(start)
        except PValidationError as err:
            self.add_error('start', str(err))
        return start

    def clean_end(self):
        """Checks validity of end date"""
        try:
            return SheduleValidator.end_validator(
                self.cleaned_data.get('start'), self.cleaned_data.get('end'))
        except PValidationError as err:
            self.add_error('end', str(err))

    class Meta:
        model = Shedule
        fields = ['start', 'end', 'quiz']
        widgets = {
            'start': DateTimePickerInput(options={'locale': 'en-gb', }),
            'end': DateTimePickerInput(options={'locale': 'en-gb', }),
        }


class InvitationForm(forms.ModelForm):
    """
    Makes URL by which users can join to group
    """

    def clean_end(self):
        """Checks validity of date"""
        try:
            return InvitationValidator.date_validator(
                self.cleaned_data.get('end'))
        except PValidationError as err:
            self.add_error('end', str(err))

    def clean_items_left(self):
        """Checks validity of invites"""
        try:
            return InvitationValidator.items_validator(
                self.cleaned_data.get('items_left'))
        except PValidationError as err:
            self.add_error('items_left', str(err))

    class Meta:
        model = Invitation
        fields = ['end', 'items_left', 'group', 'code']
        labels = {'items_left': 'Number of students:'}
        widgets = {'end': DateTimePickerInput(options={'locale': 'en-gb', }), }
