# Technical Specification: UNIX to ISO8601 Converter

## Function Specification

### Function Signature

```python
def unix_to_iso8601(timestamp: Union[int, float]) -> str:
    """
    Convert a UNIX timestamp to an ISO8601 formatted datetime string.
    
    Args:
        timestamp: UNIX timestamp (seconds since epoch) as integer or float
        
    Returns:
        ISO8601 formatted datetime string with UTC timezone
        
    Raises:
        TypeError: If timestamp is not an integer or float
        ValueError: If timestamp is invalid
    """
```

### Input Parameters

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|------------|
| timestamp | Union[int, float] | UNIX timestamp in seconds since epoch | Must be a valid numeric type |

### Output

| Type | Description | Format |
|------|-------------|--------|
| str | ISO8601 formatted datetime string | YYYY-MM-DDTHH:MM:SS.sssZ |

### Error Handling

| Error Condition | Exception | Message |
|-----------------|-----------|---------|
| timestamp is not int or float | TypeError | "Timestamp must be an integer or float" |
| timestamp is None | TypeError | "Timestamp cannot be None" |
| timestamp is invalid | ValueError | "Invalid timestamp value" |

## Implementation Details

### Algorithm

1. Validate input type (must be int or float)
2. Convert UNIX timestamp to datetime object using `datetime.datetime.fromtimestamp()`
3. Set timezone to UTC
4. Format datetime to ISO8601 string using `datetime.isoformat()`
5. Return formatted string

### Code Example

```python
from datetime import datetime, timezone
from typing import Union

def unix_to_iso8601(timestamp: Union[int, float]) -> str:
    """
    Convert a UNIX timestamp to an ISO8601 formatted datetime string.
    
    Args:
        timestamp: UNIX timestamp (seconds since epoch) as integer or float
        
    Returns:
        ISO8601 formatted datetime string with UTC timezone
        
    Raises:
        TypeError: If timestamp is not an integer or float
        ValueError: If timestamp is invalid
        
    Examples:
        >>> unix_to_iso8601(1609459200)
        '2021-01-01T00:00:00+00:00'
        >>> unix_to_iso8601(1609459200.123)
        '2021-01-01T00:00:00.123000+00:00'
    """
    if timestamp is None:
        raise TypeError("Timestamp cannot be None")
    
    if not isinstance(timestamp, (int, float)):
        raise TypeError("Timestamp must be an integer or float")
    
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.isoformat()
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid timestamp value: {e}")
```

## Edge Cases and Considerations

1. **Fractional Seconds**: The function handles float timestamps by preserving microsecond precision
2. **Timezone**: All timestamps are converted to UTC timezone for consistency
3. **Range Limitations**: Python's datetime has limitations on valid dates (typically years 1-9999)
4. **Very Large/Small Values**: Extremely large or small timestamp values may cause OverflowError

## Performance Characteristics

- **Time Complexity**: O(1) - constant time operation
- **Space Complexity**: O(1) - constant space usage
- **Dependencies**: Only Python standard library

## Testing Recommendations

1. **Unit Tests**:
   - Test with integer timestamps
   - Test with float timestamps
   - Test with edge cases (min/max valid timestamps)
   - Test error conditions

2. **Integration Tests**:
   - Test within the context of any larger application

## Usage Examples

```python
# Basic usage with integer timestamp
iso_date = unix_to_iso8601(1609459200)  # '2021-01-01T00:00:00+00:00'

# With fractional seconds
iso_date = unix_to_iso8601(1609459200.123)  # '2021-01-01T00:00:00.123000+00:00'

# Error handling
try:
    iso_date = unix_to_iso8601("not a timestamp")
except TypeError as e:
    print(f"Error: {e}")  # Error: Timestamp must be an integer or float
```