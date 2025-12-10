#!/usr/bin/env python3
import unittest
from io import StringIO
from importlib import import_module

import day02 as solution
Range = solution.Range
get_inputs = solution.get_inputs
digit_concatenations = solution.digit_concatenations
find_all_invalid_ids = solution.find_all_invalid_ids


class TestRange(unittest.TestCase):
    def test_range_contains(self):
        r = Range(10, 20)
        self.assertTrue(r.contains(10))
        self.assertTrue(r.contains(15))
        self.assertTrue(r.contains(20))
        self.assertFalse(r.contains(9))
        self.assertFalse(r.contains(21))

    def test_range_str(self):
        r = Range(11, 22)
        self.assertEqual(str(r), "11-22")


class TestGetInputs(unittest.TestCase):
    def test_single_range(self):
        input_str = "11-22\n"
        ranges = get_inputs(StringIO(input_str))
        self.assertEqual(len(ranges), 1)
        self.assertEqual(ranges[0].start, 11)
        self.assertEqual(ranges[0].end, 22)

    def test_multiple_ranges_on_one_line(self):
        input_str = "11-22,95-115,998-1012\n"
        ranges = get_inputs(StringIO(input_str))
        self.assertEqual(len(ranges), 3)
        self.assertEqual(ranges[0].start, 11)
        self.assertEqual(ranges[0].end, 22)
        self.assertEqual(ranges[1].start, 95)
        self.assertEqual(ranges[1].end, 115)
        self.assertEqual(ranges[2].start, 998)
        self.assertEqual(ranges[2].end, 1012)

    def test_example_input(self):
        input_str = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124\n"
        ranges = get_inputs(StringIO(input_str))
        self.assertEqual(len(ranges), 11)


class TestDigitConcatenations(unittest.TestCase):
    """Test finding invalid IDs (numbers made of repeated digit sequences)."""

    def test_range_95_115(self):
        """95-115 has one invalid ID, 99 (Part 1 - doubles only)."""
        r = Range(95, 115)
        invalid_ids = list(digit_concatenations(r, 2))
        self.assertEqual(set(invalid_ids), {99})

    def test_range_998_1012(self):
        """998-1012 has one invalid ID, 1010 (Part 1 - doubles only)."""
        r = Range(998, 1012)
        invalid_ids = list(digit_concatenations(r, 2))
        self.assertEqual(set(invalid_ids), {1010})

    def test_simple_examples(self):
        """Test that 55, 6464, 123123 are detected as invalid."""
        r = Range(50, 60)
        invalid_ids = list(digit_concatenations(r, 2))
        self.assertIn(55, invalid_ids)

        r = Range(6400, 6500)
        invalid_ids = list(digit_concatenations(r, 2))
        self.assertIn(6464, invalid_ids)

        r = Range(123000, 124000)
        invalid_ids = list(digit_concatenations(r, 2))
        self.assertIn(123123, invalid_ids)

    def test_no_leading_zeros(self):
        """Test that numbers like 0101 are not considered (101 is valid)."""
        r = Range(100, 110)
        invalid_ids = list(digit_concatenations(r, 2))
        # 101 is not in the list because it's not a repeated pattern
        # The only repeated pattern in range would be things like 100100, which is out of range
        self.assertNotIn(101, invalid_ids)


class TestHigherOrderRepetitions(unittest.TestCase):
    """Test that we can detect patterns repeated 2+ times."""

    def test_double_repetition(self):
        """12341234 is 1234 repeated 2 times."""
        r = Range(12341234, 12341234)
        invalid_ids = find_all_invalid_ids(r)
        self.assertIn(12341234, invalid_ids)

    def test_triple_repetition(self):
        """123123123 is 123 repeated 3 times."""
        r = Range(123123123, 123123123)
        invalid_ids = find_all_invalid_ids(r)
        self.assertIn(123123123, invalid_ids)

    def test_quintuple_repetition(self):
        """1212121212 is 12 repeated 5 times."""
        r = Range(1212121212, 1212121212)
        invalid_ids = find_all_invalid_ids(r)
        self.assertIn(1212121212, invalid_ids)

    def test_septuple_repetition(self):
        """1111111 is 1 repeated 7 times."""
        r = Range(1111111, 1111111)
        invalid_ids = find_all_invalid_ids(r)
        self.assertIn(1111111, invalid_ids)


class TestFindAllInvalidIds(unittest.TestCase):
    """Test finding all invalid IDs considering different repetition counts."""

    def test_range_includes_both_double_and_triple(self):
        """Test a range that could have both 2x and 3x repetitions."""
        r = Range(10, 111111)
        invalid_ids = find_all_invalid_ids(r)
        # Should include doubles like 11, 22, ..., 9999
        self.assertIn(11, invalid_ids)
        self.assertIn(99, invalid_ids)
        self.assertIn(1010, invalid_ids)
        # Should also include triples like 111, 222, etc.
        self.assertIn(111, invalid_ids)
        self.assertIn(222, invalid_ids)


class TestFindAllInvalidIdsPart2Examples(unittest.TestCase):
    """Test Part 2 examples with higher-order repetitions."""

    def test_range_11_22_part2(self):
        """11-22 still has two invalid IDs, 11 and 22."""
        r = Range(11, 22)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {11, 22})

    def test_range_95_115_part2(self):
        """95-115 now has two invalid IDs, 99 and 111."""
        r = Range(95, 115)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {99, 111})

    def test_range_998_1012_part2(self):
        """998-1012 now has two invalid IDs, 999 and 1010."""
        r = Range(998, 1012)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {999, 1010})

    def test_range_1188511880_1188511890_part2(self):
        """1188511880-1188511890 still has one invalid ID, 1188511885."""
        r = Range(1188511880, 1188511890)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {1188511885})

    def test_range_222220_222224_part2(self):
        """222220-222224 still has one invalid ID, 222222."""
        r = Range(222220, 222224)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {222222})

    def test_range_1698522_1698528_part2(self):
        """1698522-1698528 still contains no invalid IDs."""
        r = Range(1698522, 1698528)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), set())

    def test_range_446443_446449_part2(self):
        """446443-446449 still has one invalid ID, 446446."""
        r = Range(446443, 446449)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {446446})

    def test_range_38593856_38593862_part2(self):
        """38593856-38593862 still has one invalid ID, 38593859."""
        r = Range(38593856, 38593862)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {38593859})

    def test_range_565653_565659_part2(self):
        """565653-565659 now has one invalid ID, 565656 (56 repeated 3 times)."""
        r = Range(565653, 565659)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {565656})

    def test_range_824824821_824824827_part2(self):
        """824824821-824824827 now has one invalid ID, 824824824 (824 repeated 3 times)."""
        r = Range(824824821, 824824827)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {824824824})

    def test_range_2121212118_2121212124_part2(self):
        """2121212118-2121212124 now has one invalid ID, 2121212121 (21 repeated 5 times)."""
        r = Range(2121212118, 2121212124)
        invalid_ids = find_all_invalid_ids(r)
        self.assertEqual(set(invalid_ids), {2121212121})


if __name__ == "__main__":
    unittest.main()
