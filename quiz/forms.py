from django import forms

from quiz.models import Quizzes
from quiz.choices import TYPE_OF_QUIZ


class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=100, required=100)
    type_of_quiz = forms.ChoiceField(choices=TYPE_OF_QUIZ)

    class Meta:
        model = Quizzes

        fields = ['title', 'description', 'type_of_quiz']
