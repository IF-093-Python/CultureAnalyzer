from django import forms

from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = ['QuestionCreateForm', 'AnswerCreateForm', ]


class QuestionCreateForm(forms.ModelForm):
    """
    This Form is from creating/updating a question
    """
    quiz = forms.ModelChoiceField(queryset=Quizzes.objects.all())
    question_text = forms.TextInput()

    class Meta:
        model = Questions
        fields = ['quiz', 'question_text', ]


class AnswerCreateForm(forms.ModelForm):
    """
    This Form is from creating/updating a answer
    """
    answer_text = forms.TextInput()

    class Meta:
        model = Answers
        fields = ['answer_text', ]

    def full_clean(self):
        """
        The function validation a unique_together error from values
        'answer_text' and 'question'.
        Returns an error message if values are not unique together.
        """
        super(AnswerCreateForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except forms.ValidationError:
            self.add_error('answer_text', 'There is already a answer with '
                                          'this text in current question.')
