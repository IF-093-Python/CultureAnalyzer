from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Fieldset, Layout, Field
from tutors.models import CategoryQuestion, Question, Answer


class CategoryCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    parent_category = forms.ModelChoiceField(
        queryset=CategoryQuestion.objects.all().values_list('name', flat=True),
        required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save', css_class='btn-dark '
                                                               'mt-5'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-light mt-5',
                                     onclick="javascript:location.href = "
                                             "'/category_question';"))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Create category ',
                     css_class='border-top border-bottom mt-5'),
            Fieldset('',
                     Field('parent_category', css_class='ml-5'),
                     Field('name', css_class='ml-5'),
                     css_class='border-bottom mt-5')
        )

    class Meta:
        model = CategoryQuestion
        fields = '__all__'


class QuestionCreateForm(forms.ModelForm):
    question_text = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-question'
        self.helper.form_method = 'POST'
        self.helper.add_input(
            Submit('save', 'Save', css_class='btn-success mt-3'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-outline-success mt-3', ))
        self.helper.layout = Layout(
            Fieldset(
                'Create/Update question', css_class='display-4'),
            Fieldset('', Field('question_text'),
                     css_class='border-top border-bottom')
        )

    class Meta:
        model = Question
        fields = '__all__'


class AnswerCreateForm(forms.ModelForm):
    answer_text = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-answer'
        self.helper.form_method = 'POST'

        self.helper.add_input(Submit('save', 'Save',
                                     css_class='btn-success mt-3'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-outline-success mt-3'))
        self.helper.layout = Layout(
            Fieldset(
                'Create/Update answer', css_class='display-4'),
            Fieldset('', Field('answer_text'), css_class='border-top '
                                                         'border-bottom')
        )

    class Meta:
        model = Answer
        fields = '__all__'
