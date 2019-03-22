from django.db.utils import IntegrityError
from django.test import TestCase

from tutors.models import Questions, Answers
from quiz.models import Quizzes

__all__ = ['QuestionsModelTest', 'AnswersModelTest']


class QuestionsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.quiz_test = Quizzes.objects.create(title='Some title',
                                               description='Some description',
                                               type_of_quiz=1, )
        Questions.objects.create(quiz=cls.quiz_test,
                                 question_number=1,
                                 question_text='Some question text', )

    def test_unique_together_quiz_and_question_text(self):
        with self.assertRaises(IntegrityError) as cm:
            Questions.objects.create(quiz=self.quiz_test,
                                     question_number=2,
                                     question_text='Some question text', )
        self.assertIsInstance(cm.exception, IntegrityError)


class AnswersModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.quiz_test = Quizzes.objects.create(title='Some title',
                                               description='Some description',
                                               type_of_quiz=1, )
        cls.question_test = Questions.objects.create(quiz=cls.quiz_test,
                                                     question_number=1,
                                                     question_text='Some '
                                                                   'question '
                                                                   'text', )
        Answers.objects.create(question=cls.question_test,
                               answer_number=1,
                               answer_text='Some answer text', )

    def test_unique_together_question_and_answer_text(self):
        with self.assertRaises(IntegrityError) as cm:
            Answers.objects.create(question=self.question_test,
                                   answer_number=2,
                                   answer_text='Some answer text', )
        self.assertIsInstance(cm.exception, IntegrityError)
