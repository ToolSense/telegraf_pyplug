"""
The databases module: Functions for simplifying data requests
"""

from typing import Optional, Dict, Any, Tuple

import pymysql


def get_mysql_query_result(sql: str, config: Dict[str, Any], sql_parameters: Optional[Tuple[str, ...]] = None) -> Any:
    """
    Simplify getting data from mysql. Shouldn't be used for large data sets, as it is buffered.
    IOError is raised in case of any kind problems with database/query

    :param config:         # Required. Ex: {'user': 'root', 'passwd': 'pass', 'host': '127.0.0.1', 'port': 3306,
                           #                'db': 'information_schema', 'charset': 'utf8', 'connect_timeout': 30,}
                           # See https://pymysql.readthedocs.io/en/latest/modules/connections.html for more params

    :param sql:            # Required. Ex: 'SELECT user,COUNT(*) as cnt FROM information_schema.PROCESSLIST GROUP BY 1;'

    :param sql_parameters: # Optional. Tuple of sql query arguments. '%s' must be used as a placeholder in the query.
                           # Ex: sql: 'SELECT * from table WHERE id > %s;' sql_parameters: ('123')

    :return:               # in most cases: Optional[List[Dict[str,Any]]] Ex: [{'count': 123}]
    """
    connection: Optional[pymysql.connections.Connection] = None
    try:
        connection = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(query=sql, args=sql_parameters)
            result: Any = cursor.fetchall()

    except pymysql.Error as error:
        raise IOError(error) from None

    finally:
        if connection:
            connection.close()

    return result
