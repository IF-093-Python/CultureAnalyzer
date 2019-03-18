from django import forms


class QuestionSaveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        answers = kwargs.pop('answers')
        super(QuestionSaveForm, self).__init__(*args, **kwargs)
        choice_list = [(answer.answer_number, answer.answer_text) for answer
                       in answers]
        default_choice = self.initial.get('default_choice')
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=forms.RadioSelect(
                                                       attrs=
                                                       {'id': 'id_answers'}),
                                                   required=False,
                                                   initial=default_choice)
        self.fields['answers'].label = ''
