from django.test import TestCase
from ddt import ddt, data, unpack

from tutors.forms import QuestionCreateForm, AnswerCreateForm
from quiz.models import Quizzes

__all__ = ['QuestionFormTest', 'AnswerCreateForm', ]

_fx_question_form_data_valid = (
    (
        {
            'question_text': 'Some valid question'},
        True,
    ),
)

_fx_question_form_data_invalid = (
    (
        {'question_text': ''},
        False,
    ),
)

_fx_answer_form_data_valid = (
    (
        {'answer_text': 'Some valid answer'},
        True,
    ),
)

_fx_answer_form_data_invalid = (
    (
        {'answer_text': ''},
        False,
    ),
)


@ddt
class QuestionFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.quiz_test = Quizzes.objects.create(
            id=1,
            title='Test quiz',
            description='test description',
            type_of_quiz=1,
        )

    @unpack
    @data(*_fx_question_form_data_valid, *_fx_question_form_data_invalid)
    def test_input_data_validation_for_question(self, data_, expected):
        self.assertEqual(QuestionCreateForm(data=data_).is_valid(), expected)


@ddt
class AnswerFormTest(TestCase):

    @unpack
    @data(*_fx_answer_form_data_valid, *_fx_answer_form_data_invalid)
    def test_input_data_validation_for_answer(self, data_, expected):
        self.assertEqual(AnswerCreateForm(data=data_).is_valid(), expected)
