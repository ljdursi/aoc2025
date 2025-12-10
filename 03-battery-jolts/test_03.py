#!/usr/bin/env python3
"""
Test suite for day3 functions (max_joltage, get_inputs, parse_batteries)
"""
import unittest
from io import StringIO
from day03 import max_joltage, get_inputs, parse_batteries


class TestMaxJoltage(unittest.TestCase):
    """Test cases for the max_joltage function"""

    def _parse_battery_string(self, s: str) -> list[int]:
        """Helper method to convert a string of digits to a list of ints"""
        return [int(d) for d in s]

    def test_example_1_largest_first_two(self):
        """Test: 987654321111111 → 98"""
        batteries = self._parse_battery_string("987654321111111")
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 98)

    def test_example_2_separated_digits(self):
        """Test: 811111111111119 → 89"""
        batteries = self._parse_battery_string("811111111111119")
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 89)

    def test_example_3_last_two(self):
        """Test: 234234234234278 → 78"""
        batteries = self._parse_battery_string("234234234234278")
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 78)

    def test_example_4_complex_pattern(self):
        """Test: 818181911112111 → 92"""
        batteries = self._parse_battery_string("818181911112111")
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 92)

    def test_example_1_twelve_digits(self):
        """Test: 987654321111111 → 987654321111 (12 digits)"""
        batteries = self._parse_battery_string("987654321111111")
        result = max_joltage(batteries, 12)
        self.assertEqual(result, 987654321111)

    def test_example_2_twelve_digits(self):
        """Test: 811111111111119 → 811111111119 (12 digits)"""
        batteries = self._parse_battery_string("811111111111119")
        result = max_joltage(batteries, 12)
        self.assertEqual(result, 811111111119)

    def test_example_3_twelve_digits(self):
        """Test: 234234234234278 → 434234234278 (12 digits)"""
        batteries = self._parse_battery_string("234234234234278")
        result = max_joltage(batteries, 12)
        self.assertEqual(result, 434234234278)

    def test_example_4_twelve_digits(self):
        """Test: 818181911112111 → 888911112111 (12 digits)"""
        batteries = self._parse_battery_string("818181911112111")
        result = max_joltage(batteries, 12)
        self.assertEqual(result, 888911112111)

    def test_single_digit_selection(self):
        """Test selecting only one digit returns the maximum digit"""
        batteries = [3, 1, 4, 1, 5, 9, 2, 6]
        result = max_joltage(batteries, 1)
        self.assertEqual(result, 9)

    def test_all_digits_selection(self):
        """Test selecting all digits returns them in order"""
        batteries = [1, 2, 3]
        result = max_joltage(batteries, 3)
        self.assertEqual(result, 123)

    def test_three_digit_selection(self):
        """Test selecting three digits"""
        batteries = self._parse_battery_string("987654321")
        result = max_joltage(batteries, 3)
        self.assertEqual(result, 987)

    def test_identical_digits(self):
        """Test with all identical digits"""
        batteries = [5, 5, 5, 5, 5]
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 55)

    def test_two_digit_simple(self):
        """Test simple two digit case"""
        batteries = [1, 9, 2, 8]
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 98)

    def test_order_matters(self):
        """Test that order matters: 91 vs 19"""
        batteries = [1, 9]
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 19)

        batteries = [9, 1]
        result = max_joltage(batteries, 2)
        self.assertEqual(result, 91)

    def test_invalid_ndigits_zero(self):
        """Test that ndigits=0 raises ValueError"""
        batteries = [1, 2, 3]
        with self.assertRaises(ValueError):
            max_joltage(batteries, 0)

    def test_invalid_ndigits_negative(self):
        """Test that negative ndigits raises ValueError"""
        batteries = [1, 2, 3]
        with self.assertRaises(ValueError):
            max_joltage(batteries, -1)

    def test_invalid_ndigits_too_large(self):
        """Test that ndigits > len(batteries) raises ValueError"""
        batteries = [1, 2, 3]
        with self.assertRaises(ValueError):
            max_joltage(batteries, 4)


class TestGetInputs(unittest.TestCase):
    """Test cases for the get_inputs function"""

    def test_example_input(self):
        """Test reading the example input with four battery strings"""
        input_string = """987654321111111
811111111111119
234234234234278
818181911112111
"""
        fileobj = StringIO(input_string)
        result = get_inputs(fileobj)

        expected = [
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1],
            [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
            [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8],
            [8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1],
        ]

        self.assertEqual(result, expected)

    def test_empty_lines_skipped(self):
        """Test that empty lines are skipped"""
        input_string = """123

456

"""
        fileobj = StringIO(input_string)
        result = get_inputs(fileobj)

        expected = [
            [1, 2, 3],
            [4, 5, 6],
        ]

        self.assertEqual(result, expected)

    def test_single_line(self):
        """Test reading a single line"""
        input_string = "987654321\n"
        fileobj = StringIO(input_string)
        result = get_inputs(fileobj)

        expected = [[9, 8, 7, 6, 5, 4, 3, 2, 1]]

        self.assertEqual(result, expected)

    def test_empty_input(self):
        """Test reading empty input"""
        input_string = ""
        fileobj = StringIO(input_string)
        result = get_inputs(fileobj)

        expected = []

        self.assertEqual(result, expected)


class TestParseBatteries(unittest.TestCase):
    """Test cases for the parse_batteries function"""

    def test_simple_digit_string(self):
        """Test parsing a simple string of digits"""
        result = parse_batteries("987654321")
        expected = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(result, expected)

    def test_with_whitespace(self):
        """Test parsing a string with leading/trailing whitespace"""
        result = parse_batteries("  123456  \n")
        expected = [1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """Test parsing an empty string"""
        result = parse_batteries("")
        expected = []
        self.assertEqual(result, expected)

    def test_whitespace_only(self):
        """Test parsing a whitespace-only string"""
        result = parse_batteries("   \n\t  ")
        expected = []
        self.assertEqual(result, expected)

    def test_with_non_digit_characters(self):
        """Test that non-digit characters are filtered out"""
        result = parse_batteries("1a2b3c")
        expected = [1, 2, 3]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
