# <img alt="Telegraf_PyPlug" src="https://github.com/ToolSense/telegraf_pyplug/blob/master/logo.png">

## Problem
There is no standard way to develop Telegraf plugins in Python. Maintaining a lot of plugins designed in different ways becomes hell.

## Solution
Telegraf_pyplug is a free and open-source software library to simplify and standardize the development of python input plugins for the [Telegaf](https://github.com/influxdata/telegraf).

## Usage
```python
#!/usr/bin/env python

import datetime
import pytz

from telegraf_pyplug.common import print_influxdb_format, datetime_tzinfo_to_nano_unix_timestamp


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
    multiple_fields()
    multiple_tags()
    timestamp_add()
    timestamp_convert(datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC')))
```
More advanced examples can be found in the [examples_dir](https://github.com/ToolSense/telegraf_pyplug/tree/master/examples).

## Installation
`Telegraf_PyPlug` can easily be installed with pip.
### Mac/Linux

```bash
pip install --upgrade telegraf_pyplug
```

### Windows

```shell
python -m pip install --upgrade telegraf_pyplug
```
## License
`Telegraf_PyPlug` is under MIT license.
See the [LICENSE file](https://github.com/ToolSense/telegraf_pyplug/blob/master/LICENSE) for the full license text.