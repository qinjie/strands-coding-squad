# UNIX to ISO8601 Converter - Developer Documentation

This directory contains the development files for the UNIX to ISO8601 converter project.

## Files

- `unix_to_iso8601.py`: Main implementation of the conversion function
- `test_unix_to_iso8601.py`: Unit tests for the conversion function
- `config.py`: Configuration settings (for future extensibility)

## Implementation Summary

The implementation provides a simple, efficient function to convert UNIX timestamps to ISO8601 formatted datetime strings with UTC timezone. The function handles both integer and float timestamps, includes proper error handling, and follows PEP 8 style guidelines.

Key features:
- Converts UNIX timestamps to ISO8601 format with UTC timezone (Z suffix)
- Handles millisecond precision for float timestamps
- Provides comprehensive error handling for invalid inputs
- Includes thorough documentation with examples
- Supports negative timestamps (dates before epoch)

## Testing

The test suite covers:
- Basic functionality with integer and float timestamps
- Edge cases like epoch time (0) and negative timestamps
- Error handling for invalid inputs
- Verification of current timestamp conversion

## Future Enhancements

Potential future enhancements could include:
- Support for different output formats
- Option to specify a different timezone
- Batch processing for multiple timestamps
- Additional configuration options