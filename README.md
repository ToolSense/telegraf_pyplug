[![Build Status](https://drone.toolsense.io/api/badges/ToolSense/telegraf_pyplug/status.svg)](https://drone.toolsense.io/ToolSense/telegraf_pyplug) [![PyPI](https://img.shields.io/pypi/v/telegraf_pyplug?color=default)](https://pypi.org/project/telegraf-pyplug) [![PyPI - License](https://img.shields.io/pypi/l/telegraf_pyplug?color=default)](https://github.com/ToolSense/telegraf_pyplug/blob/master/LICENSE) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
# <img alt="Telegraf_PyPlug" src="https://github.com/ToolSense/telegraf_pyplug/blob/master/logo.png">

## Problem
[Telegaf](https://github.com/influxdata/telegraf) is a plugin-driven agent for collecting, processing, aggregating, and writing metrics.
Custom input plugins collect metrics from the system, services, or 3rd party APIs and outputs them in the [InfluxDB line protocol format](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/).
- Printing metrics in the InfluxDB line protocol format is a bit complicated, and it's easy to make mistakes.
- There is no standard way to develop Telegraf plugins in Python. Maintaining a lot of plugins designed in different ways becomes hell.

## Solution
Telegraf_pyplug is a free and open-source software library to simplify and standardize the development of python input plugins for the Telegraf.

## Usage
#### One field:
```python
from telegraf_pyplug.main import print_influxdb_format


METRIC_NAME: str = 'jumping_sheep'
METRIC_COUNT: int = 321


def main() -> None:
    print_influxdb_format(measurement=METRIC_NAME, fields={'count': METRIC_COUNT})


if __name__ == '__main__':
    main()
```
Outputs:
```text
jumping_sheep count=321
```
#### `add_timestamp` argument:
```python
from telegraf_pyplug.main import print_influxdb_format


METRIC_NAME: str = 'jumping_sheep'
METRIC_COUNT: int = 321


def main() -> None:
    print_influxdb_format(measurement=METRIC_NAME, fields={'count': METRIC_COUNT}, add_timestamp=True)


if __name__ == '__main__':
    main()
```
Outputs:
```text
jumping_sheep count=321 1599846911207090944
```
#### One field, One tag:
```python
from telegraf_pyplug.main import print_influxdb_format


METRIC_NAME: str = 'jumping_sheep'
METRIC_COUNT: int = 321
METRIC_COLOR: str = 'white'


def main() -> None:
    print_influxdb_format(measurement=METRIC_NAME, tags={'color': METRIC_COLOR}, fields={'count': METRIC_COUNT})


if __name__ == '__main__':
    main()
```
Outputs:
```text
jumping_sheep,color=white count=321
```
#### Multiple fields and tags, `nano_timestamp` argument:
```python
from datetime import datetime
from typing import Dict

from telegraf_pyplug.main import print_influxdb_format, datetime_tzinfo_to_nano_unix_timestamp


METRIC_NAME: str = 'jumping_sheep'
METRIC_FIELDS: Dict[str, int] = {'count': 321, 'height_m': 1.5}
METRIC_TAGS: Dict[str, str] = {'color': 'white', 'name': 'sweater'}
METRIC_DATE: str = '01.01.2020 03:00:00+0300'


def main() -> None:
    date: datetime = datetime.strptime(METRIC_DATE, '%d.%m.%Y %H:%M:%S%z')

    print_influxdb_format(
        measurement=METRIC_NAME,
        tags=METRIC_TAGS,
        fields=METRIC_FIELDS,
        nano_timestamp=datetime_tzinfo_to_nano_unix_timestamp(date)
    )


if __name__ == '__main__':
    main()
```
Outputs:
```text
jumping_sheep,color=white,name=sweater count=321,height_m=1.5 1577836800000000000
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