"""
Configuration settings for the unix_to_iso8601 module.
"""

# Default configuration settings
DEFAULT_CONFIG = {
    # ISO8601 format configuration
    "iso8601": {
        # Whether to include milliseconds in the output
        "include_milliseconds": True,
        # Default timezone (UTC)
        "timezone": "UTC",
    },
    
    # Validation settings
    "validation": {
        # Maximum allowed timestamp value (year 9999)
        "max_timestamp": 253402300799,  # 9999-12-31T23:59:59Z
        # Minimum allowed timestamp value (year 0001)
        "min_timestamp": -62135596800,  # 0001-01-01T00:00:00Z
    }
}

# Note: These settings are not currently used in the implementation
# but are provided for future extensibility.