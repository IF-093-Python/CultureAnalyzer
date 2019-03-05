from django.test import TestCase

import datetime

from quiz.models import Quizzes
from groups.forms import SheduleForm


class SheduleFormTest(TestCase):

    def test_valid_shedule_form(self):
        quiz = Quizzes.objects.create()
        form = SheduleForm(data={
            'begin': datetime.datetime.now() + datetime.timedelta(days=1),
            'end': datetime.datetime.now() + datetime.timedelta(days=2),
            'quiz': quiz.pk
        })
        self.assertTrue(form.is_valid())

    def test_invalid_shedule_form(self):
        form = SheduleForm(data={
            'begin': datetime.datetime.now() + datetime.timedelta(days=1),
            'end': datetime.datetime.now() + datetime.timedelta(days=2),
            'quiz': ''
        })
        self.assertFalse(form.is_valid())

    def test_invalid_shedule_form_begin_after_past(self):
        quiz = Quizzes.objects.create()
        form = SheduleForm(data={
            'begin': datetime.datetime.now() + datetime.timedelta(days=2),
            'end': datetime.datetime.now() + datetime.timedelta(days=1),
            'quiz': quiz.pk
        })
        self.assertFalse(form.is_valid())

    def test_invalid_shedule_form_begin_less_then_now(self):
        quiz = Quizzes.objects.create()
        form = SheduleForm(data={
            'begin': datetime.datetime.now() - datetime.timedelta(days=1),
            'end': datetime.datetime.now() + datetime.timedelta(days=1),
            'quiz': quiz.pk
        })
        self.assertFalse(form.is_valid())
