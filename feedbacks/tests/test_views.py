from ddt import ddt, data
from django.test import TestCase
from django.urls import reverse

from feedbacks.tests_data.test_view_data import PAGE_STRING_VALUES
from feedbacks.tests_data.test_form_data import (
    FEEDBACK_MIN_VALUE_IS_GREATER_MAX_VALUE_DATA,
)
from feedbacks.tests.mixins import (FeedbackCRUDViewsSetUpMixin,
                                    RecommendationCRUDViewsSetUpMixin,
                                    SetUpUserMixin, USERNAME, PASSWORD)
from feedbacks.models import Feedback

__all__ = ['FeedbackListViewTest', ]


@ddt
class FeedbackListViewTest(SetUpUserMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
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
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('feedback-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/feedback_list.html')

    @data(*range(-10, 1))
    def test_call_view_where_page_number_less_then_1(self, page):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=1')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)

    @data(*range(10, 21))
    def test_call_view_where_page_number_is_to_large(self, page):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=2')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)

    @data(*PAGE_STRING_VALUES)
    def test_call_view_where_page_number_not_int(self, page):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f'{reverse("feedback-list")}?page={page}')
        expected_response = self.client.get(
            f'{reverse("feedback-list")}?page=1')
        self.assertEqual(response.status_code, expected_response.status_code)
        self.assertEqual(response.rendered_content,
                         expected_response.rendered_content)


class FeedbackDeleteViewTest(FeedbackCRUDViewsSetUpMixin, TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('feedback-delete', kwargs={'pk': 1}))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-delete", kwargs={"pk": 1})}')
        response = self.client.post(reverse('feedback-delete',
                                            kwargs={'pk': 1}))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-delete", kwargs={"pk": 1})}')

    def test_redirect_to_feedback_list_on_success(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(reverse('feedback-delete',
                                            kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('feedback-list'))


@ddt
class FeedbackUpdateViewTest(FeedbackCRUDViewsSetUpMixin, TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('feedback-update', kwargs={'pk': 1}))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-update", kwargs={"pk": 1})}')
        response = self.client.post(reverse('feedback-update',
                                            kwargs={'pk': 1}))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-update", kwargs={"pk": 1})}')

    def test_uses_correct_template(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('feedback-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/feedback_form.html')

    @data(*FEEDBACK_MIN_VALUE_IS_GREATER_MAX_VALUE_DATA)
    def test_form_invalid_max_less_min(self, feedback_data):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            reverse('feedback-update', kwargs={'pk': 1}), feedback_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'min_value',
                             'Min value must be less then max value')


@ddt
class FeedbackCreateViewTest(FeedbackCRUDViewsSetUpMixin, TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('feedback-create'))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-create")}')
        response = self.client.post(reverse("feedback-create"))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("feedback-create")}')

    def test_uses_correct_template(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse("feedback-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/feedback_form.html')

    @data(*FEEDBACK_MIN_VALUE_IS_GREATER_MAX_VALUE_DATA)
    def test_form_invalid_max_less_min(self, feedback_data):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(reverse("feedback-create"), feedback_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'min_value',
                             'Min value must be less then max value')


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
        self.client.login(username=USERNAME, password=PASSWORD)
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
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            reverse('recommendation-update', kwargs={'pk': 1}),
            {'recommendation': 'Another recommendation'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('feedback-detail', kwargs={'pk': 1}))

    def test_uses_correct_template(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('recommendation-update',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/recommendation_form.html')


@ddt
class RecommendationCreateViewTest(RecommendationCRUDViewsSetUpMixin, TestCase):

    def test_get_create_with_missing_feedback_argument(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('recommendation-create'))
        self.assertEqual(response.status_code, 400)

    @data(*range(2, 12))
    def test_get_create_with_wrong_feedback_argument(self, feedback_id):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(
            f'{reverse("recommendation-create")}?feedback={feedback_id}')
        self.assertEqual(response.status_code, 400)

    def test_get_create_with_valid_feedback_argument(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(
            f'{reverse("recommendation-create")}?feedback={1}')
        self.assertEqual(response.status_code, 200)

    def test_post_create_with_valid_feedback_argument(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            f'{reverse("recommendation-create")}?feedback={1}',
            {'recommendation': 'Second recommendation'})
        self.assertEqual(response.status_code, 302)

    @data(*range(2, 12))
    def test_post_create_with_invalid_feedback_argument(self, feedback_id):
        self.client.login(username=USERNAME, password=PASSWORD)
        with self.assertRaises(Feedback.DoesNotExist):
            self.client.post(
                f'{reverse("recommendation-create")}?feedback={feedback_id}',
                {'recommendation': 'Second recommendation'})
