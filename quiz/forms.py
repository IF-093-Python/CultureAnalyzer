from django import forms

from quiz.models import Quizzes


class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=100, required=100)

    class Meta:
        model = Quizzes

        fields = ['title', 'description']
