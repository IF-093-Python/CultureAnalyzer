from django.test import TestCase, tag
from django.utils import timezone
from ddt import ddt, data

from quiz.models import Quizzes
from groups.models import Group
from groups.forms import SheduleForm, InvitationForm

from groups.tests_data.test_form_data import *


@tag('fast')
@ddt
class SheduleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for a in range(100):
            Quizzes.objects.create()

    @data(*shedule_valid_data())
    def test_valid_shedule_form(self, value):
        form = SheduleForm(data=value)
        self.assertTrue(form.is_valid())

    @data(*shedule_invalid_data())
    def test_invalid_shedule_form_without_quiz(self, value):
        form = SheduleForm(data=value)
        if value['start'] > value['end'] or value['start'] < timezone.now():
            self.assertFalse(form.is_valid())
        else:
            self.assertTrue(form.is_valid())


@tag('fast')
@ddt
class InvitationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for a in range(100):
            Group.objects.create()

    @data(*invitation_valid_data())
    def test_valid_invitation_form(self, value):
        form = InvitationForm(data=value)
        self.assertTrue(form.is_valid())

    @data(*invitation_invalid_data())
    def test_invalid_invitation_form_without_group(self, value):
        form = InvitationForm(data=value)
        if value['end'] < timezone.now() or value['items_left'] == 0:
            self.assertFalse(form.is_valid())
        else:
            self.assertTrue(form.is_valid())