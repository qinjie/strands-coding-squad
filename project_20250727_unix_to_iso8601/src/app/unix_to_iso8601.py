"""
Unix Timestamp to ISO8601 Converter

This module provides functionality to convert UNIX timestamps to ISO8601 formatted datetime strings.
"""

from datetime import datetime, timezone
from typing import Union, Optional


def unix_to_iso8601(timestamp: Union[int, float]) -> str:
    """
    Convert a UNIX timestamp to an ISO8601 formatted datetime string with UTC timezone.

    Args:
        timestamp: A UNIX timestamp (seconds since epoch) as integer or float.

    Returns:
        str: ISO8601 formatted datetime string with UTC timezone (Z suffix).

    Raises:
        TypeError: If the input is not an integer or float.
        ValueError: If the timestamp is too large to be processed or otherwise invalid.

    Examples:
        >>> unix_to_iso8601(1609459200)
        '2021-01-01T00:00:00Z'
        >>> unix_to_iso8601(1609459200.5)
        '2021-01-01T00:00:00.500000Z'
        >>> unix_to_iso8601(0)
        '1970-01-01T00:00:00Z'
        >>> unix_to_iso8601(-86400)  # One day before epoch
        '1969-12-31T00:00:00Z'
    """
    # Type checking
    if not isinstance(timestamp, (int, float)):
        raise TypeError("Timestamp must be an integer or float")

    try:
        # Convert timestamp to datetime object with UTC timezone
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        # Format to ISO8601 string with Z suffix for UTC
        return dt.isoformat().replace('+00:00', 'Z')
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid timestamp: {e}")


if __name__ == "__main__":
    # Simple demonstration
    import time
    current_timestamp = time.time()
    print(f"Current timestamp: {current_timestamp}")
    print(f"ISO8601 format: {unix_to_iso8601(current_timestamp)}")