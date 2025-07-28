# Functional Specification

## Function Signature
`convert_unix_to_iso(timestamp: Union[int, float]) -> str`

## Parameters
- `timestamp`: UNIX epoch time (seconds since 1970-01-01T00:00:00Z)

## Returns
- ISO8601 formatted string with UTC timezone (e.g., 2023-01-01T00:00:00Z)

## Behavior
1. Accepts integer/float inputs
2. Converts to UTC timezone
3. Handles microsecond precision for floats
4. Returns empty string for invalid inputs