import datetime
import io
import unittest
import unittest.mock
from typing import Dict, Any, List, Union

import pytz

from telegraf_pyplug.common import print_influxdb_format, is_str_repr_of_int, datetime_tzinfo_to_nano_unix_timestamp


PRINT_INFLUXDB_FORMAT_TEST_DATA: List[Dict[str, Any]] = [
    # field float repr of int
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f': 123}
        },
        'expected': 'm f=123\n'
    },
    # field float repr of float
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f': 123.123}
        },
        'expected': 'm f=123.123\n'
    },
    # field int
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f': '123i'}
        },
        'expected': 'm f=123i\n'
    },
    # field str
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f': '123'}
        },
        'expected': 'm f="123"\n'
    },
    # field bool
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'t1': 'true', 't2': 'True', 't3': 'TRUE', 't4': 't', 't5': 'T', 't6': True,
                       'f1': 'false', 'f2': 'False', 'f3': 'FALSE', 'f4': 'f', 'f5': 'F', 'f6': False}
        },
        'expected': 'm t1=true,t2=True,t3=TRUE,t4=t,t5=T,t6=True,f1=false,f2=False,f3=FALSE,f4=f,f5=F,f6=False\n'
    },
    # field multiple
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1, 'f2': 2, 'f3': 3}
        },
        'expected': 'm f1=1,f2=2,f3=3\n'
    },
    # field str with '"'
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': '"str_in_double_quote"'}
        },
        'expected': 'm f1="\\"str_in_double_quote\\""\n'
    },
    # tag int, float, str
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1, 'f2': 2, 'f3': 3},
            'tags': {'int': 1, 'float': 2.2, 'str': 'abc'}},
        'expected': 'm,int=1,float=2.2,str=abc f1=1,f2=2,f3=3\n'
    },
    # tag multiple
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1, 'f2': 2, 'f3': 3},
            'tags': {'t1': 1, 't2': 2, 't3': 3}
        },
        'expected': 'm,t1=1,t2=2,t3=3 f1=1,f2=2,f3=3\n'
    },
    # tag str special chars
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1},
            'tags': {'t1': 's p a c e', 't2': 'com,ma', 't3': 'equ=al', 't4': 'quo"te'}},
        'expected': 'm,t1=s\\ p\\ a\\ c\\ e,t2=com\\,ma,t3=equ\\=al,t4=quo"te f1=1\n'
    },
    # nano_timestamp
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1},
            'nano_timestamp': 1597688387675328768,
        },
        'expected': 'm f1=1 1597688387675328768\n'
    },
    # add_timestamp
    {
        'arguments': {
            'measurement': 'm',
            'fields': {'f1': 1},
            'add_timestamp': True,
        },
        'expected': 'm f1=1 1577836800000000000\n'
    },
]

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


class TestPrintInfluxdbFormat(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, arguments, expected_output, mock_stdout):
        with unittest.mock.patch('telegraf_pyplug.common.utc_now',
                                 return_value=datetime.datetime(2020, 1, 1, 0, 0, 0, 0, pytz.timezone("UTC"))):
            print_influxdb_format(**arguments)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_over_test_cases(self):
        for test_case in PRINT_INFLUXDB_FORMAT_TEST_DATA:
            with self.subTest(test_case=test_case):
                self.assert_stdout(  # pylint: disable=no-value-for-parameter
                    test_case.get('arguments'),
                    test_case.get('expected')
                )


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
