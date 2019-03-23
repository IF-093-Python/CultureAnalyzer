from unittest import TestCase
from ddt import ddt, data, unpack

from indicators.tests_data.test_models_data import INDICATORS_DATA

__all__ = ['CountryIndicatorTest']


@ddt
class CountryIndicatorTest(TestCase):

    @unpack
    @data(*INDICATORS_DATA)
    def test_get_indicators_with_object_name(self,
                                             data_obj,
                                             expected_indicators,
                                             expected_str):
        self.assertEqual(str(data_obj), expected_str)

        indicator_res = data_obj.get_indicators
        keys_length = 1
        self.assertEqual(len(indicator_res.keys()), keys_length)
        self.assertIn(data_obj.iso_code, indicator_res.keys())
        self.assertEqual(indicator_res[data_obj.iso_code], expected_indicators)
