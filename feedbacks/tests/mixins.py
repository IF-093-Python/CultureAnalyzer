from django.contrib.auth import get_user_model
from django.urls import reverse

from feedbacks.models import Feedback, Recommendation

__all__ = ['FeedbackCRUDViewsSetUpMixin', 'RecommendationCRUDViewsSetUpMixin',
           'SetUpUserMixin', 'FeedbackPageRetrieverMixin', 'USERNAME', 'PASSWORD']

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
        self.feedback_pk = Feedback.objects.get(pk=1).id
        self.recommendation_pk = Recommendation.objects.create(
            recommendation='Lorem ipsum', feedback_id=self.feedback_pk).id


class FeedbackCRUDViewsSetUpMixin(SetUpUserMixin):

    def setUp(self):
        self.pk = Feedback.objects.create(feedback='Some text',
                                          min_value=0,
                                          max_value=10,
                                          indicator='PDI').id


class FeedbackPageRetrieverMixin(object):

    def get_feedback_page(self, page):
        return self.client.get(f'{reverse("feedback-list")}?page={page}')
