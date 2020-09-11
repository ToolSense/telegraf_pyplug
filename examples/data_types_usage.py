#!/usr/bin/env python

from telegraf_pyplug.main import print_influxdb_format


def multiple_fields() -> None:
    """
    Prints line:
    multiple_fields field_float=1,field_int=123i,field_str="two",field_bool=True
    """
    print_influxdb_format(
        measurement='multiple_fields',
        fields={
            'field_float': 1,
            'field_int': '123i',
            'field_str': 'two',
            'field_bool': True,
        }
    )


def multiple_tags() -> None:
    """
    Prints line:
    multiple_tags,tag1=1,tag2=two field_name=123
    """
    print_influxdb_format(
        measurement='multiple_tags',
        fields={'field_name': 123},
        tags={
            'tag1': 1,  # tags are always strings
            'tag2': 'two'
        }
    )


if __name__ == '__main__':
    multiple_fields()
    multiple_tags()
