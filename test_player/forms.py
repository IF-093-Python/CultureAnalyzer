from django import forms


class QuestionSaveForm(forms.Form):

    def __init__(self, answers, default_choice, *args, **kwargs):
        super(QuestionSaveForm, self).__init__(*args, **kwargs)
        choice_list = [(answer.id, answer.answer_text) for answer in answers]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=forms.RadioSelect,
                                                   required=False,
                                                   initial=default_choice)
