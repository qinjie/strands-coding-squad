# UNIX to ISO8601 Converter

A simple Python utility for converting UNIX timestamps to ISO8601 formatted datetime strings.

## Overview

This library provides a straightforward function to convert UNIX timestamps (seconds since epoch) to ISO8601 formatted datetime strings with UTC timezone.

## Installation

No special installation is required. Simply include the `unix_to_iso8601.py` file in your project.

## Usage

```python
from app.unix_to_iso8601 import unix_to_iso8601

# Convert a UNIX timestamp to ISO8601
iso_date = unix_to_iso8601(1609459200)  # Returns '2021-01-01T00:00:00Z'

# Convert a timestamp with milliseconds
iso_date = unix_to_iso8601(1609459200.5)  # Returns '2021-01-01T00:00:00.500000Z'

# Convert current time
import time
current_time = unix_to_iso8601(time.time())
```

## Features

- Converts UNIX timestamps to ISO8601 formatted strings
- Handles both integer and float timestamps
- Includes proper UTC timezone designation (Z suffix)
- Provides comprehensive error handling
- Supports negative timestamps (dates before epoch)
- Follows PEP 8 style guidelines

## Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## Testing

Run the tests using:

```bash
python -m unittest src/tests/test_unix_to_iso8601.py
```