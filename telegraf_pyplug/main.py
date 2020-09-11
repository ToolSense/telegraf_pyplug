"""
The main module: print functions
"""

from typing import Optional, Union, Dict, List

from telegraf_pyplug.util import datetime_tzinfo_to_nano_unix_timestamp, is_str_repr_of_int, utc_now


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
