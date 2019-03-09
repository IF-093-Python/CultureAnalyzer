from ddt import ddt, data
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from feedbacks.tests_data.test_view_data import PAGE_STRING_VALUES
from feedbacks.models import Feedback, Recommendation

__all__ = ['FeedbackListViewTest', ]


class RecommendationCRUDViewsSetUpMixin(object):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user', password='test')
        Feedback.objects.create(feedback='Some text', min_value=0, max_value=10,
                                indicator='PDI')

    def setUp(self):
        feedback = Feedback.objects.get(pk=1)
        Recommendation.objects.create(recommendation='Lorem ipsum',
                                      feedback=feedback)


@ddt
class FeedbackListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user', password='test')
        for i in range(10):
            Feedback.objects.create(feedback='Some text', min_value=i,
                                    max_value=i + 5, indicator='PDI')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('feedback-list'), follow=True)
        self.assertRedirects(response,
                             f'/login/?next={reverse("feedback-list")}')
        response = self.client.post(reverse('feedback-list'), follow=True)
        self.assertRedirects(response,
                             f'/login/?next={reverse("feedback-list")}')

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')
        response = self.client.get(reverse('feedback-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/feedback_list.html')

    @data(*range(-10, 1))
    def test_call_view_where_page_number_less_then_1(self, page):
        self.client.login(username='user', password='test')
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=1')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)

    @data(*range(10, 21))
    def test_call_view_where_page_number_is_to_large(self, page):
        self.client.login(username='user', password='test')
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=2')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)

    @data(*PAGE_STRING_VALUES)
    def test_call_view_where_page_number_not_int(self, page):
        self.client.login(username='user', password='test')
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=1')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)


class RecommendationDeleteViewTest(RecommendationCRUDViewsSetUpMixin, TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('recommendation-delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(
            response,
            f'/login/?next={reverse("recommendation-delete", kwargs={"pk": 1})}')
        response = self.client.post(
            reverse('recommendation-delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(
            response,
            f'/login/?next={reverse("recommendation-delete", kwargs={"pk": 1})}')

    def test_redirects_to_related_feedback(self):
        self.client.login(username='user', password='test')
        response = self.client.post(
            reverse('recommendation-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('feedback-detail', kwargs={'pk': 1}))


class RecommendationUpdateViewTest(RecommendationCRUDViewsSetUpMixin, TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('recommendation-update', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(
            response,
            f'/login/?next={reverse("recommendation-update", kwargs={"pk": 1})}')
        response = self.client.post(
            reverse('recommendation-update', kwargs={'pk': 1}),
            {'recommendation': 'Another recommendation'}, follow=True)
        self.assertRedirects(
            response,
            f'/login/?next={reverse("recommendation-update", kwargs={"pk": 1})}')

    def test_redirects_to_related_feedback(self):
        self.client.login(username='user', password='test')
        response = self.client.post(
            reverse('recommendation-update', kwargs={'pk': 1}),
            {'recommendation': 'Another recommendation'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('feedback-detail', kwargs={'pk': 1}))

    def test_uses_correct_template(self):
        self.client.login(username='user', password='test')
        response = self.client.get(reverse('recommendation-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/recommendation_form.html')
