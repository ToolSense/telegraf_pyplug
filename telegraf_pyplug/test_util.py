import datetime
import unittest.mock
from typing import Dict, List, Union

import pytz

from telegraf_pyplug.util import is_str_repr_of_int, datetime_tzinfo_to_nano_unix_timestamp


IS_STR_REPR_OF_INT_TEST_DATA: List[Dict[str, Union[str, bool]]] = [
    {'arguments': '123', 'expected': False},
    {'arguments': '123i', 'expected': True},
    {'arguments': 'i', 'expected': False},
    {'arguments': '-i', 'expected': False},
    {'arguments': '+i', 'expected': False},
    {'arguments': '1f', 'expected': False},
    {'arguments': '0i', 'expected': True},
    {'arguments': '0', 'expected': False},
    {'arguments': '+0', 'expected': False},
    {'arguments': '-0', 'expected': False},
    {'arguments': '-0i', 'expected': True},
    {'arguments': '+0i', 'expected': True},
    {'arguments': '_0i', 'expected': False},
    {'arguments': 'a0i', 'expected': False},
    {'arguments': '-a0i', 'expected': False},
    {'arguments': '+a0i', 'expected': False},
    {'arguments': '+=0i', 'expected': False},
]


class TestIsStrReprOfInt(unittest.TestCase):
    def test_over_test_cases(self):
        for test_case in IS_STR_REPR_OF_INT_TEST_DATA:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    is_str_repr_of_int(test_case.get('arguments')),
                    test_case.get('expected')
                )


class TestDatetimeTzinfoToNanoUnixTimestamp(unittest.TestCase):
    def test_utc(self):
        self.assertEqual(
            datetime_tzinfo_to_nano_unix_timestamp(
                pytz.timezone("UTC").localize(datetime.datetime(2020, 1, 1, 0, 0, 0, 0))
            ),
            1577836800 * 1000 * 1000 * 1000
        )

    def test_msk(self):
        self.assertEqual(
            datetime_tzinfo_to_nano_unix_timestamp(
                pytz.timezone("Europe/Moscow").localize(datetime.datetime(2020, 1, 1, 3, 0, 0, 0))
            ),
            1577836800 * 1000 * 1000 * 1000

        )

    def test_est(self):
        self.assertEqual(
            datetime_tzinfo_to_nano_unix_timestamp(
                pytz.timezone("EST").localize(datetime.datetime(2019, 12, 31, 19, 0, 0, 0))
            ),
            1577836800 * 1000 * 1000 * 1000
        )
