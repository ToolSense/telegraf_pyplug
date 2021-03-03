#!/usr/bin/env python

"""
Example of Postgres plugin for Telegraf.
Returns a count of open connections grouped by user in the InfluxDB format.
"""

import sys
import socket
from typing import Dict, Union, List, NamedTuple, Optional

from telegraf_pyplug.main import print_influxdb_format
from telegraf_pyplug.db import get_postgres_query_result


POSTGRES_CONFIG: Dict[str, Union[str, int]] = {
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'postgres',
}

SQL: str = """
    SELECT usename,count(*) FROM pg_stat_activity WHERE usename IS NOT NULL GROUP BY 1;
"""

HOST = socket.gethostname()


def main() -> None:
    """
    Prints lines like those:
    postgres_open_connections,host=server123,user=user1 value=2
    postgres_open_connections,host=server123,user=user2 value=1
    postgres_open_connections,host=server123,user=user3 value=7
    """
    try:
        data: List[Optional[NamedTuple]] = get_postgres_query_result(sql=SQL, config=POSTGRES_CONFIG)
        if data is None:
            sys.exit('Error: Empty response from DB')
        try:
            for record in data:
                user: str = str(getattr(record, 'usename', 'unknown'))
                count: int = int(getattr(record, 'count', 0))
                print_influxdb_format(
                    measurement='postgres_open_connections',
                    tags={'host': HOST, 'user': user},
                    fields={'value': count},
                )
        except (IndexError, KeyError, ValueError):
            sys.exit('Error: Unexpected response from DB')

    except IOError as error:
        sys.exit(error)


if __name__ == '__main__':
    main()
