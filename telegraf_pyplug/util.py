"""
The utils module: Secondary/auxiliary functions
"""

import datetime

import pytz


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
