from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Fieldset, Layout
from tutors.models import Question, Answer


class QuestionCreateForm(forms.ModelForm):
    question_text = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-question-create'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save', css_class='btn-dark'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-light'))
        # onclick="javascript:location.href = '/question-list';"))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Create question', 'question_text')
        )

    class Meta:
        model = Question


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
            Fieldset('Create answer', 'answer_text')
        )

    class Meta:
        model = Answer
