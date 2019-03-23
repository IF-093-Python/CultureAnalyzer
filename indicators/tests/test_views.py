from django.test import TestCase
from ddt import ddt, data, unpack
from django.urls import reverse

from CultureAnalyzer.constants import ADMIN_ID
from indicators.tests.util import create_user_with_role, USERNAME, PASSWORD
from indicators.tests_data.test_views_data import SEARCH_DATA

__all__ = ['CountryIndicatorListViewTest', 'CountryIndicatorUpdateTest']


@ddt
class CountryIndicatorListViewTest(TestCase):

    fixtures = ['indicators/tests_data/test_data.json']
    test_url = reverse('country_indicator:country_indicator_list')

    @classmethod
    def setUpTestData(cls):
        permissions = ('view_countryindicator',)
        create_user_with_role(ADMIN_ID, permissions)

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_indicators_result_list_view(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 5)

        page_number = 2
        response = self.client.get(f'{self.test_url}?page={page_number}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    @unpack
    @data(*SEARCH_DATA)
    def test_search_results(self, search_value, expected_count,
                            expected_iso_code_list):
        response = self.client.get(f"{self.test_url}?indicator_search"
                                   f"={search_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), expected_count,
                         msg=f'Incorrect expected length of result with search'
                             f': {search_value}')

        iso_list = [field.iso_code for field in response.context['indicators']]
        self.assertEqual(iso_list, expected_iso_code_list,
                         msg=f'Incorrect order with search: {search_value}')


class CountryIndicatorUpdateTest(TestCase):

    fixtures = ['indicators/tests_data/test_data.json']

    @classmethod
    def setUpTestData(cls):
        permissions = ('change_countryindicator', 'add_countryindicator')
        create_user_with_role(ADMIN_ID, permissions)

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_context_data(self):
        test_url = reverse('country_indicator:country_indicator_update',
                           kwargs={'pk': 9})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['update'])

        response = self.client.get(reverse(
            'country_indicator:country_indicator_create'))
        self.assertFalse('update' in response.context.keys())
