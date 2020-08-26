"""
The common module: Shared functions, classes
"""

from typing import Optional, Union, Dict, Any, Tuple, List
import datetime

import pymysql
import pytz


def get_mysql_query_result(sql: str, config: Dict[str, Any], sql_parameters: Optional[Tuple[str, ...]] = None) -> Any:
    """
    Return Optional[List[Dict[str,Any]]].
    IOError is raised in case of any kind problems with database/query
    """
    connection: Optional[pymysql.connections.Connection] = None
    try:
        connection = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(query=sql, args=sql_parameters)
            result: Any = cursor.fetchall()

    except pymysql.Error as error:
        raise IOError('Unexpected mysql error') from error

    finally:
        if connection:
            connection.close()

    return result


def datetime_tzinfo_to_nano_unix_timestamp(date_time: datetime.datetime) -> int:
    """
    Converts datetime WITH TZINFO to nano unix timestamp
    """
    return round(date_time.astimezone(pytz.timezone('UTC')).timestamp() * 1000 * 1000 * 1000)


def is_str_repr_of_int(string: str) -> bool:
    """
    Returns True for strings like: '123i', '+123i', '-123i'
    """
    if string.startswith('-') or string.startswith('+'):
        if string[1:-1].isdigit() and string.endswith('i'):
            return True
    if string[0:-1].isdigit() and string.endswith('i'):
        return True

    return False


def utc_now() -> datetime.datetime:
    """
    Returns datetime.datetime with UTC tzinfo
    """
    return datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))


def print_influxdb_format(
        measurement: str,
        fields: Dict[str, Union[str, int, float]],
        tags: Optional[Dict[str, Union[str, int, float]]] = None,
        nano_timestamp: Optional[int] = None,
        add_timestamp: bool = False,
) -> None:
    """
    Prints data in InfluxDB line protocol format.
    Ex:
        print_influxdb_format(
            measurement='modules_reboots',
            fields={'value': 123},
            tags={'reboot_reason': 2},
        )
    Stdout:
        modules_reboots,reboot_reason=2 value=123


    :param measurement:     # Required. Please use only characters "a-z", numbers and "_". Ex: 'electricity'

    :param fields:          # Required. Ex: {'voltage_v': 220, 'current_a': 10}
    :param tags:            # Optional. Ex: {'type': 'ac', 'power_line_no': 123}

    :param nano_timestamp:  # Optional timestamp value. Must be in nanoseconds.
                            # Please use the datetime_tzinfo_to_nano_unix_timestamp function to convert.

    :param add_timestamp:   # Adds the current timestamp in nanoseconds.
    """

    result: str = f'{measurement}'

    if tags:
        for tag_name, tag_value in tags.items():
            if isinstance(tag_value, str):
                tag_value = tag_value.strip()
                tag_value = tag_value.replace(' ', r'\ ')
                tag_value = tag_value.replace(',', r'\,')
                tag_value = tag_value.replace('=', r'\=')

            result += f',{tag_name}={tag_value}'

    fields_list: List[str] = []
    for field_name, field_value in fields.items():
        if isinstance(field_value, str):
            field_value = field_value.strip()
            if field_value not in ['true', 'True', 'TRUE', 't', 'T', 'false', 'False', 'FALSE', 'f', 'F', ]:
                if not is_str_repr_of_int(field_value):
                    field_value = field_value.replace('"', '\\"')
                    field_value = f'"{field_value}"'

        fields_list.append(f'{field_name}={field_value}')
    result += f' {",".join(fields_list)}'

    if nano_timestamp:
        result += f' {nano_timestamp}'
    elif add_timestamp:
        result += f' {datetime_tzinfo_to_nano_unix_timestamp(utc_now())}'

    print(result)
