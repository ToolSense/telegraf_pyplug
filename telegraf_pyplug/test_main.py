import datetime
import io
import unittest
import unittest.mock
from typing import Dict, Any, List

import pytz

from telegraf_pyplug.main import print_influxdb_format


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


class TestPrintInfluxdbFormat(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, arguments, expected_output, mock_stdout):
        with unittest.mock.patch('telegraf_pyplug.main.utc_now',
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
