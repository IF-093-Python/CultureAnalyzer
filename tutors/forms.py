from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Fieldset, Layout, Field
from tutors.models import Question, Answer


class QuestionCreateForm(forms.ModelForm):
    question_text = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-question'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save', css_class='btn-success '
                                                               'mt-3'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-outline-success mt-3',
                                     onclick="javascript:location.href = '/question';"))
        self.helper.layout = Layout(
            Fieldset(
                'Create/Update question', css_class='display-4'),
            Fieldset('', Field('question_text'), css_class='border-top border-bottom')
            )

    class Meta:
        model = Question
        fields = ['question_text', ]


class AnswerCreateForm(forms.ModelForm):
    answer_text = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-answer-create'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save', css_class='btn-dark'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-light'))
        # onclick="javascript:location.href = '/answer-list';"))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Create answer',
                     Field('answer_text', css_class='border-top'))
            )

    class Meta:
        model = Answer
        fields = ['question', 'answer_text', ]
