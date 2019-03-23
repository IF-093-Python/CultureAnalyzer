from django.test import TestCase
from ddt import ddt, data, unpack

from CultureAnalyzer.constants import ADMIN_ID
from indicators.tests.util import create_user_with_role, USERNAME, PASSWORD
from indicators.tests_data.test_views_data import SEARCH_DATA

__all__ = ['CountryIndicatorListViewTest', 'CountryIndicatorUpdateTest']


@ddt
class CountryIndicatorListViewTest(TestCase):

    fixtures = ['indicators/tests_data/test_data.json']

    @classmethod
    def setUpTestData(cls):
        permissions = ('view_countryindicator',)
        create_user_with_role(ADMIN_ID, permissions)

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_indicators_result_list_view(self):
        response = self.client.get("/indicators/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 5)

        response = self.client.get("/indicators/?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    @unpack
    @data(*SEARCH_DATA)
    def test_search_results(self, search_value, expected_count,
                            expected_iso_code_list):
        response = self.client.get(f"/indicators/?indicator_search"
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
        response = self.client.get("/indicators/9/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['update'])

        response = self.client.get("/indicators/create/")
        self.assertFalse('update' in response.context.keys())
