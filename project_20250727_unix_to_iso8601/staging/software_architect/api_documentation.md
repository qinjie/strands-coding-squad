# API Documentation: UNIX to ISO8601 Converter

## Function: `unix_to_iso8601`

Converts a UNIX timestamp (seconds since epoch) to an ISO8601 formatted datetime string with UTC timezone.

### Signature

```python
def unix_to_iso8601(timestamp: Union[int, float]) -> str
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `timestamp` | `int` or `float` | Yes | UNIX timestamp in seconds since epoch (e.g., 1609459200) |

### Return Value

| Type | Description | Example |
|------|-------------|---------|
| `str` | ISO8601 formatted datetime string with UTC timezone | `'2021-01-01T00:00:00+00:00'` |

### Exceptions

| Exception | Condition |
|-----------|-----------|
| `TypeError` | If `timestamp` is not an integer or float, or if it's `None` |
| `ValueError` | If `timestamp` is an invalid value that cannot be converted to a datetime |

### Examples

#### Basic Usage

```python
from datetime_utils import unix_to_iso8601

# Convert integer timestamp
iso_date = unix_to_iso8601(1609459200)
print(iso_date)  # Output: '2021-01-01T00:00:00+00:00'

# Convert float timestamp with fractional seconds
iso_date = unix_to_iso8601(1609459200.123)
print(iso_date)  # Output: '2021-01-01T00:00:00.123000+00:00'
```

#### Error Handling

```python
from datetime_utils import unix_to_iso8601

try:
    # Invalid type
    iso_date = unix_to_iso8601("1609459200")
except TypeError as e:
    print(f"Error: {e}")  # Output: Error: Timestamp must be an integer or float

try:
    # None value
    iso_date = unix_to_iso8601(None)
except TypeError as e:
    print(f"Error: {e}")  # Output: Error: Timestamp cannot be None

try:
    # Invalid timestamp value (too large)
    iso_date = unix_to_iso8601(10**20)
except ValueError as e:
    print(f"Error: {e}")  # Output: Error: Invalid timestamp value: ...
```

### Notes

1. The function always returns the datetime in UTC timezone (indicated by the `+00:00` suffix)
2. Fractional seconds in the input timestamp are preserved in the output string
3. The function uses Python's standard library and has no external dependencies
4. Valid timestamp range is limited by Python's datetime module (typically years 1-9999)

### Integration

This function can be imported and used in any Python module:

```python
# Import the function
from datetime_utils import unix_to_iso8601

# Use in your code
def process_event(event_data):
    event_time = unix_to_iso8601(event_data['timestamp'])
    # Further processing...
```