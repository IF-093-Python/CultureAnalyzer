from django import forms

from quiz.models import Quizzes, TYPE_OF_QUIZ


class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    description = forms.TextInput()
    type_of_quiz = forms.ChoiceField(choices=TYPE_OF_QUIZ)

    class Meta:
        model = Quizzes
        fields = ['title', 'description', 'type_of_quiz']
