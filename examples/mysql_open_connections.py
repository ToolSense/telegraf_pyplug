#!/usr/bin/env python

"""
Example of Mysql plugin for Telegraf.
Returns a count of open connections grouped by user in the InfluxDB format.
"""

import sys
import socket
from typing import Dict, Union, List

from telegraf_pyplug.main import print_influxdb_format
from telegraf_pyplug.db import get_mysql_query_result


MYSQL_CONFIG: Dict[str, Union[str, int]] = {
    'user': 'mysql_user',
    'passwd': 'mysql_pass',
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'information_schema',
    'charset': 'utf8',
    'connect_timeout': 30,
}

SQL: str = """
    SELECT 
        user,
        COUNT(*) as count
    FROM
        information_schema.PROCESSLIST
    GROUP BY
        1;
"""

HOST = socket.gethostname()


def main() -> None:
    """
    Prints lines like those:
    mysql_open_connections,host=server123,user=user1 value=2
    mysql_open_connections,host=server123,user=user2 value=1
    mysql_open_connections,host=server123,user=user3 value=7
    """
    try:
        data: List[Dict[str, Union[str, int]]] = get_mysql_query_result(sql=SQL, config=MYSQL_CONFIG)
        if data is None:
            sys.exit('Error: Empty response from DB')
        try:
            for value in data:
                user: str = str(value['user'])
                count: int = int(value['count'])
                print_influxdb_format(
                    measurement='mysql_open_connections',
                    tags={'host': HOST, 'user': user},
                    fields={'value': count},
                )
        except (IndexError, KeyError, ValueError):
            sys.exit('Error: Unexpected response from DB')

    except IOError as error:
        sys.exit(error)


if __name__ == '__main__':
    main()
