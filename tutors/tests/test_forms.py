from django.test import TestCase

from tutors.forms import QuestionCreateForm, AnswerCreateForm
from quiz.models import Quizzes


class QuestionFormTest(TestCase):

    def setUp(self):
        self.quiz_test = Quizzes.objects.create(title='Test quiz',
                                                description='test description',
                                                type_of_quiz=1)

    def test_valid_form(self):
        form = QuestionCreateForm(data={
            'quiz': self.quiz_test.id,
            'question_text': 'Some valid question',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_quiz_form(self):
        form = QuestionCreateForm(data={
            'quiz': 15,
            'question_text': 'Some invalid question',
        })
        self.assertFalse(form.is_valid())

    def test_invalid_text_form(self):
        form = QuestionCreateForm(data={
            'quiz': self.quiz_test.id,
            'question_text': '',
        })
        self.assertFalse(form.is_valid())


class AnswerFormTest(TestCase):

    def test_valid_form(self):
        form = AnswerCreateForm(data={
            'answer_text': 'Some valid answer',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_text_form(self):
        form = AnswerCreateForm(data={
            'question_text': '',
        })
        self.assertFalse(form.is_valid())
