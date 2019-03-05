from django.utils import timezone
from django import forms
import datetime

from groups.models import Group, Shedule
from users.models import CustomUser
from quiz.models import Quizzes
from bootstrap_datepicker_plus import DateTimePickerInput

__all__ = ['GroupCreateForm', 'GroupUpdateForm', 'SheduleForm', ]


class GroupCreateForm(forms.ModelForm):
    mentor = forms.ModelMultipleChoiceField(
        label='Mentors of group:', queryset=CustomUser.objects.all(),
        required=False)

    class Meta:
        model = Group
        fields = ['name', 'mentor']


class GroupUpdateForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(
        label='Users in group:',
        queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Group
        fields = ['user']


class SheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SheduleForm, self).__init__(*args, **kwargs)
        date = timezone.now()
        quizzes = Quizzes.objects.order_by('type_of_quiz', 'title')
        self.fields['begin'].initial = date
        self.fields['end'].initial = date
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quizzes,
                                                     initial=quizzes.first())

    def clean(self):
        cleaned_data = super(SheduleForm, self).clean()
        start = cleaned_data.get("begin")
        end = cleaned_data.get("end")
        if cleaned_data.get("begin") < \
                (timezone.now()+timezone.timedelta(minutes=1)):
            msg = u"Start date already passed! Please enter valid date."
            self.add_error('begin', msg)
            raise forms.ValidationError(msg)
        if start > end:
            msg = u"End date should be after start date!"
            self.add_error('end', msg)
            raise forms.ValidationError(msg)
        return cleaned_data

    class Meta:
        model = Shedule
        fields = ['begin', 'end', 'quiz']
        widgets = {
            'begin': DateTimePickerInput(options={
                                         'locale': 'en-gb',
                                         }),
            'end': DateTimePickerInput(options={
                                         'locale': 'en-gb',
                                         }),
        }
