from django.test import TestCase

from quiz.service import (get_average_results, check_group_indicators,
                          get_indicators_values)
from quiz.tests_data.test_service_data import (get_random_data,
                                               get_group_random_data,
                                               VALID_MAX_VALUE,
                                               VALID_MIN_VALUE,
                                               NUMBER_OF_QUESTION,
                                               INVALID_MIN_VALUE,
                                               INVALID_MAX_VALUE)


class TestService(TestCase):

    def test_user_average_data_return_24_results(self):
        self.assertEqual(len(get_average_results([
            get_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                            NUMBER_OF_QUESTION)])), 24)

    def test_group_average_data_return_24_results(self):
        self.assertEqual(len(get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION))), 24)

    def test_method_returns_6_indicators(self):
        avg_data = get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION))
        indicators = get_indicators_values(avg_data)
        self.assertEqual(len(indicators), 6)

    def test_method_return_right_indicator_values(self):
        avg_data = get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION))
        indicators = get_indicators_values(avg_data)

        self.assertTrue(all(100 >= i >= 0 for i in
                            check_group_indicators(indicators).values()))

    def test_method_return_right_indicator_for_wrong_value(self):
        avg_data = get_average_results(
            get_group_random_data(INVALID_MIN_VALUE, INVALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION))
        indicators = get_indicators_values(avg_data)

        self.assertTrue(all(100 >= i >= 0 for i in
                            check_group_indicators(indicators).values()))
