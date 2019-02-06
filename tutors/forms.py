from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, Field, HTML
from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = [
    'QuestionCreateForm',
    'AnswerCreateForm',
]


class QuestionCreateForm(forms.ModelForm):
    """
    This Form is from creating/updating a question
    """
    quiz = forms.ModelChoiceField(queryset=Quizzes.objects.all())
    question_text = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-question'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'Create/Update question', css_class='display-4'),
            Fieldset('', Field('quiz'),
                     css_class='border-top border-bottom'),
            Fieldset('',
                     Field('question_text'),
                     css_class='border-top border-bottom'),
            Fieldset('',
                     Submit('save', 'Save', css_class='btn-success mt-3'),
                     HTML(
                         """<a class='btn btn-outline-success mt-3' href="
                         {%url 'tutors:questions_list'%}">Cancel</a>"""),
                     )
        )

    class Meta:
        model = Questions
        fields = ['quiz', 'question_text', ]


class AnswerCreateForm(forms.ModelForm):
    """
    This Form is from creating/updating a answer
    """
    answer_text = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-answer'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'Create/Update answer', css_class='display-4'),
            Fieldset('', Field('answer_text', ),
                     Field('question', ),
                     css_class='border-top border-bottom'),
            Fieldset('',
                     Submit('save', 'Save', css_class='btn-success mt-3'),
                     HTML("""<a class='btn btn-outline-success mt-3' href="
                     {%url 'tutors:answers_list' question_id=q.id%}">Cancel
                     </a>"""),
                     )
        )

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
        except forms.ValidationError as e:
            self._update_errors(e)
