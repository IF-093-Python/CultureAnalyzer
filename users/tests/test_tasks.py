import uuid
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.test import TestCase as DjangoTestCase
from unittest import mock

from users.tasks import clear_expired_sessions
from users.tests.utils import (mock_datetime_now, tz_datetime,
                               mock_datetime_from)


def mock_tasks_datetime_now(**kwargs):
    return mock_datetime_now("users.tasks.datetime", **kwargs)


class TaskClearSessionsTest(DjangoTestCase):
    @mock_tasks_datetime_now(year=2018, month=1, day=1)
    def test_clear_expired_sessions_where_some_expired(self):
        old_and_expired = tz_datetime(year=2017, month=1, day=1)
        new_and_not_expired = tz_datetime(year=2018, month=2, day=1)
        self.generate_sessions(old_and_expired, limit=10)
        self.generate_sessions(new_and_not_expired, limit=3)
        clear_expired_sessions()
        self.assertIs(Session.objects.count(), 3)

    @mock_tasks_datetime_now(year=2019, month=1, day=1)
    def test_clear_expired_sessions_where_all_expired(self):
        all_expired = tz_datetime(year=2017, month=1, day=1)
        self.generate_sessions(all_expired, limit=30)
        clear_expired_sessions()
        self.assertIs(Session.objects.count(), 0)

    @mock_tasks_datetime_now(year=2019, month=3, day=10, hour=12)
    def test_clear_expired_sessions_where_all_not_expired(self):
        all_not_expired = tz_datetime(year=2019, month=3, day=10, hour=13)
        self.generate_sessions(all_not_expired, limit=5,
                               days_interval=0, hours_interval=2)
        clear_expired_sessions()
        self.assertIs(Session.objects.count(), 5)

    @mock.patch("users.tasks.datetime")
    def test_emulate_expire_sessions(self, datetime_mock):
        stage1 = mock_datetime_from(year=2020, month=8, day=1)
        stage2 = mock_datetime_from(year=2020, month=9, day=11)
        stage3 = mock_datetime_from(year=2020, month=9, day=14)
        stage4 = mock_datetime_from(year=2020, month=9, day=20)

        # Generate 5 sessions(exp=[(3)|(6)|(9)|(12)|(15)].09.2020)
        # Expected on stages:
        # 1. Delete 0, keep 5 sessions(exp=[(3)|(6)|(9)|(12)|(15)].09.2020)
        # 2. Delete 3, keep 2 sessions(exp=[(9)|(12)|(15)].09.2020)
        # 3. Delete 1, keep 1 sessions(exp=15.09.2020)
        # 4. Delete 1, keep 0 sessions
        self.generate_sessions(
            initial_datetime=tz_datetime(year=2020, month=9, day=1),
            days_interval=3,
            limit=5
        )

        self.assertIs(Session.objects.count(), 5)
        self.assertSessionsCountAfterClearIs(5, datetime_mock, stage1)
        self.assertSessionsCountAfterClearIs(2, datetime_mock, stage2)
        self.assertSessionsCountAfterClearIs(1, datetime_mock, stage3)
        self.assertSessionsCountAfterClearIs(0, datetime_mock, stage4)

    def assertSessionsCountAfterClearIs(self, expected,
                                        datetime_to_mock, mock_now_value):
        datetime_to_mock.now = mock_now_value
        clear_expired_sessions()
        self.assertIs(Session.objects.count(), expected)

    def generate_sessions(self, initial_datetime, days_interval=1,
                          minutes_interval=0, hours_interval=0, limit=5):
        expire_date = initial_datetime
        for i in range(0, limit):
            random_key = uuid.uuid4().hex[0:35]
            expire_date += timedelta(days=days_interval,
                                     hours=hours_interval,
                                     minutes=minutes_interval)
            Session.objects.create(session_key=random_key,
                                   expire_date=expire_date)
