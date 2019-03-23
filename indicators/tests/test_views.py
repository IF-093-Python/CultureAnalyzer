from django.test import TestCase
from ddt import ddt, data, unpack

from indicators.tests.util import create_user_with_role, USERNAME, PASSWORD

__all__ = ['CountryIndicatorListViewTest', 'CountryIndicatorUpdateTest']


_search_data = (
        ('bra', 1, ['BRA']),
        ('an', 3, ['ALB', 'FRA', 'GER']),
        ('ukr', 1, ['UKR']),
        ('France', 1, ['FRA']),
        ('Ukraine', 1, ['UKR']),
        ('tuy', 0, []),
        ('Frynce', 0, []),
        (' fj 9', 0, [])
    )


@ddt
class CountryIndicatorListViewTest(TestCase):

    fixtures = ['indicators/tests_data/test_data.json']

    @classmethod
    def setUpTestData(cls):
        role_name = 'Admin'
        permissions = ('view_countryindicator',)
        create_user_with_role(role_name, permissions)

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
    @data(*_search_data)
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
        role_name = 'Admin'
        permissions = ('change_countryindicator', 'add_countryindicator')
        create_user_with_role(role_name, permissions)

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_context_data(self):
        response = self.client.get("/indicators/9/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['update'])

        response = self.client.get("/indicators/create/")
        self.assertFalse('update' in response.context.keys())
