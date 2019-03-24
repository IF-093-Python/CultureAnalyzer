from django.test import TestCase

from quiz.service import (get_average_results, check_group_indicators,
                          get_indicators_values,
                          NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ,
                          MIN_INDICATOR_VALUE,
                          MAX_INDICATOR_VALUE)
from quiz.tests_data.test_service_data import (get_random_data,
                                               get_group_random_data,
                                               VALID_MAX_VALUE,
                                               VALID_MIN_VALUE,
                                               NUMBER_OF_QUESTION,
                                               INVALID_MIN_VALUE,
                                               INVALID_MAX_VALUE)


class TestService(TestCase):

    def test_user_average_data(self):
        self.assertEqual(len(get_average_results([
            get_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                            NUMBER_OF_QUESTION)],
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)

    def test_group_average_data(self):
        self.assertEqual(len(get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)

    def test_get_average_results_method(self):
        avg_data = get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)
        indicators = get_indicators_values(avg_data)
        self.assertEqual(len(indicators), 6)

    def test_get_indicators_values_method_with_valid_data(self):
        avg_data = get_average_results(
            get_group_random_data(VALID_MIN_VALUE, VALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)
        indicators = get_indicators_values(avg_data)

        self.assertFalse(
            any(not MIN_INDICATOR_VALUE <= i <= MAX_INDICATOR_VALUE for i in
                check_group_indicators(indicators).values()))

    def test_get_indicators_values_method_with_invalid_data(self):
        avg_data = get_average_results(
            get_group_random_data(INVALID_MIN_VALUE, INVALID_MAX_VALUE,
                                  NUMBER_OF_QUESTION),
            NUMBER_OF_QUESTION_FOR_BUSINESS_QUIZ)
        indicators = get_indicators_values(avg_data)

        self.assertFalse(
            any(not MIN_INDICATOR_VALUE <= i <= MAX_INDICATOR_VALUE for i in
                check_group_indicators(indicators).values()))
