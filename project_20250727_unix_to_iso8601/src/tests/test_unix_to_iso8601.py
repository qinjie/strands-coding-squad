"""
Tests for the unix_to_iso8601 function.
"""

import unittest
import sys
import os
from datetime import datetime, timezone

# Add the parent directory to the path so we can import the app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.unix_to_iso8601 import unix_to_iso8601


class TestUnixToISO8601(unittest.TestCase):
    """Test cases for the unix_to_iso8601 function."""

    def test_integer_timestamp(self):
        """Test conversion of integer timestamp."""
        # 2021-01-01T00:00:00Z
        self.assertEqual(unix_to_iso8601(1609459200), "2021-01-01T00:00:00Z")

    def test_float_timestamp(self):
        """Test conversion of float timestamp with milliseconds."""
        # 2021-01-01T00:00:00.500000Z
        self.assertEqual(unix_to_iso8601(1609459200.5), "2021-01-01T00:00:00.500000Z")

    def test_epoch_timestamp(self):
        """Test conversion of epoch timestamp (0)."""
        self.assertEqual(unix_to_iso8601(0), "1970-01-01T00:00:00Z")

    def test_negative_timestamp(self):
        """Test conversion of negative timestamp (before epoch)."""
        # One day before epoch
        self.assertEqual(unix_to_iso8601(-86400), "1969-12-31T00:00:00Z")

    def test_current_timestamp(self):
        """Test conversion of current timestamp."""
        # Get current timestamp
        current_timestamp = datetime.now(timezone.utc).timestamp()
        # Convert to ISO8601
        iso8601_str = unix_to_iso8601(current_timestamp)
        # Parse back to datetime for comparison (avoiding millisecond precision issues)
        dt = datetime.fromisoformat(iso8601_str.replace('Z', '+00:00'))
        # Check if the timestamps are close (within 1 second)
        self.assertAlmostEqual(dt.timestamp(), current_timestamp, delta=1)

    def test_type_error(self):
        """Test that TypeError is raised for non-numeric inputs."""
        with self.assertRaises(TypeError):
            unix_to_iso8601("not a number")
        
        with self.assertRaises(TypeError):
            unix_to_iso8601(None)

    def test_value_error(self):
        """Test that ValueError is raised for invalid timestamps."""
        # Extremely large timestamp that should cause an overflow
        with self.assertRaises(ValueError):
            unix_to_iso8601(2**64)


if __name__ == "__main__":
    unittest.main()