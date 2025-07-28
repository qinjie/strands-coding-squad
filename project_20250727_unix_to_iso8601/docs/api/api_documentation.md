# API Documentation

## `unix_to_iso8601` Function

### Description

Converts a UNIX timestamp (seconds since epoch) to an ISO8601 formatted datetime string with UTC timezone.

### Signature

```python
def unix_to_iso8601(timestamp: Union[int, float]) -> str:
```

### Parameters

- `timestamp` (Union[int, float]): A UNIX timestamp (seconds since epoch) as integer or float.

### Returns

- `str`: ISO8601 formatted datetime string with UTC timezone (Z suffix).

### Exceptions

- `TypeError`: If the input is not an integer or float.
- `ValueError`: If the timestamp is too large to be processed or otherwise invalid.

### Examples

```python
# Convert a specific date (January 1, 2021)
unix_to_iso8601(1609459200)  # Returns '2021-01-01T00:00:00Z'

# Convert with millisecond precision
unix_to_iso8601(1609459200.5)  # Returns '2021-01-01T00:00:00.500000Z'

# Convert epoch time
unix_to_iso8601(0)  # Returns '1970-01-01T00:00:00Z'

# Convert a date before epoch
unix_to_iso8601(-86400)  # Returns '1969-12-31T00:00:00Z'
```

### Implementation Details

The function uses Python's `datetime` module to convert the UNIX timestamp to a datetime object with UTC timezone, then formats it according to the ISO8601 standard.

The ISO8601 format used is: `YYYY-MM-DDThh:mm:ss.sssZ` where:
- `YYYY-MM-DD` is the date part
- `T` is the separator between date and time
- `hh:mm:ss.sss` is the time part (with optional milliseconds)
- `Z` indicates UTC timezone (Zulu time)