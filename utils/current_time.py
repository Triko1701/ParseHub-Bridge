from datetime import datetime
import pytz

def get_current_time(tz: str) -> datetime:
    """
    Get the current date and time in the specified timezone.

    Parameters:
    - tz (str): A string representing the timezone, e.g., 'UTC', 'America/New_York', 'Europe/London', etc.

    Returns:
    - datetime: A datetime object representing the current date and time in the specified timezone.

    Example:
    >>> get_current_time('UTC')
    datetime.datetime(2024, 1, 15, 12, 30, 0, tzinfo=<UTC>)
    """
    tz = pytz.timezone(tz)
    current_time = datetime.now(tz)
    return current_time
