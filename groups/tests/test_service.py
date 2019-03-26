import pytz
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core import mail
from django.test import TestCase
from django.conf import settings

from groups.models import Shedule, Group
from quiz.models import Quizzes

USERNAME_MENTOR = 'mentor'
USERNAME_USER = 'user'
PASSWORD = '123456'
EMAIL_MENTOR = 'mentor@gmail.com'
EMAIL_USER = 'user@gmail.com'


class EmailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            pk=1,
            username=USERNAME_MENTOR,
            password=PASSWORD,
            email=EMAIL_MENTOR)
        get_user_model().objects.create_user(
            pk=2,
            username=USERNAME_USER,
            password=PASSWORD,
            email=EMAIL_USER)
        cls.group_test = Group.objects.create(
            name='Test group',)
        cls.group_test.user.set(get_user_model().objects.filter(pk=2))
        cls.group_test.mentor.set(get_user_model().objects.filter(pk=1))
        cls.schedule_test = Shedule.objects.create(
            start=datetime(2019, 3, 27, 12, 0, tzinfo=pytz.UTC),
            end=datetime(2019, 4, 27, 12, 0, tzinfo=pytz.UTC),
            quiz=Quizzes.objects.create(
                title='Test quiz',
                description='Some description',
                type_of_quiz=1,
            ),
            group=cls.group_test,
        )

    def test_send_email_to_mentor(self):
        email_from = settings.EMAIL_HOST_USER
        for mentor in self.group_test.mentor.all():
            mail.send_mail(
                self.group_test.name,
                'Here is the message',
                email_from,
                [mentor.email, ],
                fail_silently=False,
            )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Test group')
        self.assertEqual(mail.outbox[0].to, [EMAIL_MENTOR])

    def test_send_email_to_member(self):
        email_from = settings.EMAIL_HOST_USER
        for member in self.group_test.user.all():
            mail.send_mail(
                self.schedule_test.quiz.title,
                'Here is the message',
                email_from,
                [member.email, ],
                fail_silently=False,
            )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Test quiz')
        self.assertEqual(mail.outbox[0].to, [EMAIL_USER])
