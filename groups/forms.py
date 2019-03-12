from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.utils import timezone

from groups.models import Group, Shedule, Invitation
from quiz.models import Quizzes

__all__ = ['GroupCreateForm', 'GroupUpdateForm', 'SheduleForm', ]


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'mentor']
        widgets = {'mentor': forms.CheckboxSelectMultiple(), }


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['user']
        widgets = {'mentor': forms.CheckboxSelectMultiple(), }


class SheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SheduleForm, self).__init__(*args, **kwargs)
        quizzes = Quizzes.objects.order_by('type_of_quiz', 'title')
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quizzes,
                                                     initial=quizzes.first())

    def clean(self):
        cleaned_data = super(SheduleForm, self).clean()
        start = cleaned_data.get('begin')
        end = cleaned_data.get('end')
        if start < timezone.now():
            msg = u'Start date already passed! Please enter valid date.'
            self.add_error('begin', msg)
        if start >= end:
            msg = u'End date should be after start date!'
            self.add_error('end', msg)
        return cleaned_data

    class Meta:
        model = Shedule
        fields = ['begin', 'end', 'quiz']
        widgets = {
            'begin': DateTimePickerInput(options={'locale': 'en-gb', }),
            'end': DateTimePickerInput(options={'locale': 'en-gb', }),
        }


class InvitationForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(InvitationForm, self).clean()
        start = cleaned_data.get('begin')
        end = cleaned_data.get('end')
        if end < timezone.now():
            msg = u'End date already passed! Please enter valid date.'
            self.add_error('end', msg)
        if start >= end:
            msg = u'End date should be after start date!'
            self.add_error('end', msg)
        return cleaned_data

    class Meta:
        model = Invitation
        fields = ['start', 'end', 'items_left']
        labels = {'items_left': 'items'}
        widgets = {
            'begin': DateTimePickerInput(options={'locale': 'en-gb', }),
            'end': DateTimePickerInput(options={'locale': 'en-gb', }),
        }
