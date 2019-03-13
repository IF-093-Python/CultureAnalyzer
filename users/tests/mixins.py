from django.contrib.auth import get_user_model

__all__ = ['SetUpMixin']


USERNAME = 'TestUser'
PASSWORD = 'test_qwerty'


class SetUpMixin(object):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username=USERNAME,
                                             password=PASSWORD)
