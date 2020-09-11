#!/usr/bin/env python

import datetime
import pytz

from telegraf_pyplug.main import print_influxdb_format
from telegraf_pyplug.util import datetime_tzinfo_to_nano_unix_timestamp


def timestamp_add() -> None:
    """
    Prints line like this:
    timestamp_add,color=green value=123 1598903300806018048
    """
    print_influxdb_format(
        measurement='timestamp_add',
        fields={'value': 123},
        tags={'color': 'green'},
        add_timestamp=True
    )


def timestamp_convert(datetime_tz: datetime.datetime) -> None:
    """
    Prints line like this:
    timestamp_convert,color=green value=123 1577836800000000000
    """
    print_influxdb_format(
        measurement='timestamp_convert',
        fields={'value': 123},
        tags={'color': 'green'},
        nano_timestamp=datetime_tzinfo_to_nano_unix_timestamp(datetime_tz)
    )


if __name__ == '__main__':
    timestamp_add()
    timestamp_convert(datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC')))
