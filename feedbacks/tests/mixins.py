from django.contrib.auth import get_user_model

from feedbacks.models import Feedback, Recommendation

__all__ = ['FeedbackCRUDViewsSetUpMixin', 'RecommendationCRUDViewsSetUpMixin',
           'SetUpUserMixin', 'USERNAME', 'PASSWORD']

USERNAME = 'test_user'
PASSWORD = '12345'


class SetUpUserMixin(object):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username=USERNAME,
                                             password=PASSWORD)


class RecommendationCRUDViewsSetUpMixin(SetUpUserMixin):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Feedback.objects.create(feedback='Some text', min_value=0, max_value=10,
                                indicator='PDI')

    def setUp(self):
        feedback = Feedback.objects.get(pk=1)
        Recommendation.objects.create(recommendation='Lorem ipsum',
                                      feedback=feedback)


class FeedbackCRUDViewsSetUpMixin(SetUpUserMixin):

    def setUp(self):
        Feedback.objects.create(feedback='Some text', min_value=0, max_value=10,
                                indicator='PDI')
