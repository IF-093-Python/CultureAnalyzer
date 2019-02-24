from datetime import datetime
from django import forms

from groups.models import Group, DateOfQuiz
from users.models import CustomUser
from quiz.models import Quizzes
from bootstrap_datepicker_plus import DateTimePickerInput

__all__ = ['GroupCreateForm','GroupUpdateForm','SetQuizForGroupForm',]


class GroupCreateForm(forms.ModelForm):
    mentor = forms.ModelMultipleChoiceField(
        label='Mentors of group:', queryset=CustomUser.objects.all(),
        required=False)

    class Meta:
        model = Group
        fields = ['name', 'mentor']



class GroupUpdateForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(
        label='Users in group:',queryset=CustomUser.objects.all(),required=False)

    class Meta:
        model = Group
        fields = ['user']



class SetQuizForGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SetQuizForGroupForm, self).__init__(*args, **kwargs)
        date = datetime.now()
        quizzes = Quizzes.objects.order_by('type_of_quiz', 'title')
        self.fields['begin'].initial = date
        self.fields['end'].initial = date
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quizzes,
                                                     initial=quizzes[0])


    def clean(self):
        cleaned_data = super(SetQuizForGroupForm, self).clean()
        start = cleaned_data.get("begin").strftime('%Y-%m-%d %H:%M:%S')
        end = cleaned_data.get("end").strftime('%Y-%m-%d %H:%M:%S')
        if start > end:
            msg = u"End date should be after start date!"
            self.add_error('end',msg)
            raise forms.ValidationError(msg)
        print('Data from form:')
        print(cleaned_data)
        return cleaned_data

    class Meta:
        model = DateOfQuiz
        fields = ['begin','end','quiz']
        widgets = {
            'begin': DateTimePickerInput(options={
                                         'locale': 'en-gb',
                                         }),
            'end': DateTimePickerInput(options={
                                         'locale': 'en-gb',
                                         }),
        }