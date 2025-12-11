#!/usr/bin/env python3
"""
Unit tests for Advent of Code 2025 - Day 5: Cafeteria inventory freshness
"""

import unittest
import io
from day05 import Range, contained_in_ranges, get_inputs, merge_ranges


class TestRange(unittest.TestCase):
    """Test cases for the Range class."""

    def test_init(self):
        """Test basic Range initialization."""
        r = Range(3, 5)
        self.assertEqual(r.start, 3)
        self.assertEqual(r.end, 5)

    def test_from_tuple(self):
        """Test Range construction from tuple."""
        r = Range.from_tuple((10, 14))
        self.assertEqual(r.start, 10)
        self.assertEqual(r.end, 14)

    def test_from_str(self):
        """Test Range construction from string."""
        r = Range.from_str("16-20")
        self.assertEqual(r.start, 16)
        self.assertEqual(r.end, 20)

    def test_from_str_custom_separator(self):
        """Test Range construction from string with custom separator."""
        r = Range.from_str("12:18", sep=":")
        self.assertEqual(r.start, 12)
        self.assertEqual(r.end, 18)

    def test_valid_str_valid(self):
        """Test valid_str with valid range strings."""
        self.assertTrue(Range.valid_str("3-5"))
        self.assertTrue(Range.valid_str("10-14"))
        self.assertTrue(Range.valid_str("1-1"))

    def test_valid_str_invalid(self):
        """Test valid_str with invalid range strings."""
        self.assertFalse(Range.valid_str("5"))  # No separator
        self.assertFalse(Range.valid_str("5-3-2"))  # Too many parts

    def test_str_representation(self):
        """Test string representation of Range."""
        r = Range(3, 5)
        self.assertEqual(str(r), "3-5")

    def test_contains_inside_range(self):
        """Test contains method with value inside range."""
        r = Range(3, 5)
        self.assertTrue(r.contains(3))
        self.assertTrue(r.contains(4))
        self.assertTrue(r.contains(5))

    def test_contains_outside_range(self):
        """Test contains method with value outside range."""
        r = Range(3, 5)
        self.assertFalse(r.contains(2))
        self.assertFalse(r.contains(6))
        self.assertFalse(r.contains(0))
        self.assertFalse(r.contains(100))

    def test_contains_boundary_values(self):
        """Test contains method with boundary values."""
        r = Range(10, 14)
        self.assertTrue(r.contains(10))  # Lower boundary
        self.assertTrue(r.contains(14))  # Upper boundary
        self.assertFalse(r.contains(9))  # Just below
        self.assertFalse(r.contains(15))  # Just above

    def test_single_value_range(self):
        """Test range with single value (start == end)."""
        r = Range(7, 7)
        self.assertTrue(r.contains(7))
        self.assertFalse(r.contains(6))
        self.assertFalse(r.contains(8))

    def test_repr_representation(self):
        """Test repr representation of Range."""
        r = Range(3, 5)
        self.assertEqual(repr(r), "Range(3, 5)")

    def test_hash_identical_ranges(self):
        """Test that identical ranges have the same hash."""
        r1 = Range(1, 10)
        r2 = Range(1, 10)
        self.assertEqual(hash(r1), hash(r2))

    def test_hash_different_ranges(self):
        """Test that different ranges have different hashes."""
        r1 = Range(1, 10)
        r2 = Range(1, 11)
        self.assertNotEqual(hash(r1), hash(r2))

    def test_range_in_set(self):
        """Test that ranges can be used in sets."""
        ranges = {Range(1, 5), Range(10, 15), Range(1, 5)}
        self.assertEqual(len(ranges), 2)  # Duplicate removed

    def test_range_as_dict_key(self):
        """Test that ranges can be used as dictionary keys."""
        d = {Range(1, 5): "first", Range(10, 15): "second"}
        self.assertEqual(d[Range(1, 5)], "first")

    def test_length(self):
        """Test length method."""
        self.assertEqual(Range(1, 5).length(), 5)
        self.assertEqual(Range(10, 14).length(), 5)
        self.assertEqual(Range(7, 7).length(), 1)
        self.assertEqual(Range(1, 100).length(), 100)


class TestRangeErrorHandling(unittest.TestCase):
    """Test cases for Range error handling."""

    def test_invalid_range_start_greater_than_end(self):
        """Test that creating a range with start > end raises ValueError."""
        with self.assertRaises(ValueError):
            Range(10, 5)

    def test_valid_str_with_non_numeric(self):
        """Test valid_str with non-numeric strings."""
        self.assertFalse(Range.valid_str("abc-def"))
        self.assertFalse(Range.valid_str("1-abc"))
        self.assertFalse(Range.valid_str("abc-2"))

    def test_valid_str_with_inverted_range(self):
        """Test valid_str with inverted range (start > end)."""
        self.assertFalse(Range.valid_str("10-5"))

    def test_equality_with_non_range(self):
        """Test equality comparison with non-Range objects."""
        r = Range(1, 5)
        self.assertNotEqual(r, "1-5")
        self.assertNotEqual(r, (1, 5))
        self.assertNotEqual(r, 5)
        self.assertNotEqual(r, None)


class TestRangeComparison(unittest.TestCase):
    """Test cases for Range comparison operators."""

    def test_equality_same_ranges(self):
        """Test equality with identical ranges."""
        r1 = Range(1, 10)
        r2 = Range(1, 10)
        self.assertEqual(r1, r2)

    def test_equality_different_ranges(self):
        """Test equality with different ranges."""
        r1 = Range(1, 10)
        r2 = Range(1, 11)
        r3 = Range(2, 10)
        self.assertNotEqual(r1, r2)
        self.assertNotEqual(r1, r3)

    def test_less_than_different_starts(self):
        """Test less-than comparison with different start values."""
        r1 = Range(1, 10)
        r2 = Range(5, 15)
        self.assertTrue(r1 < r2)
        self.assertFalse(r2 < r1)

    def test_less_than_same_starts(self):
        """Test less-than comparison with same start values."""
        r1 = Range(5, 10)
        r2 = Range(5, 15)
        # Both have same start, so r1 < r2 should be False
        self.assertFalse(r1 < r2)
        self.assertFalse(r2 < r1)

    def test_sorting_ranges(self):
        """Test that ranges can be sorted by start value."""
        ranges = [Range(10, 15), Range(1, 5), Range(20, 25), Range(5, 8)]
        sorted_ranges = sorted(ranges)
        self.assertEqual(sorted_ranges[0], Range(1, 5))
        self.assertEqual(sorted_ranges[1], Range(5, 8))
        self.assertEqual(sorted_ranges[2], Range(10, 15))
        self.assertEqual(sorted_ranges[3], Range(20, 25))


class TestRangeOverlaps(unittest.TestCase):
    """Test cases for Range.overlaps method."""

    def test_overlaps_standard_overlap(self):
        """Test standard overlapping ranges."""
        r1 = Range(1, 17)
        r2 = Range(13, 29)
        self.assertTrue(r1.overlaps(r2))
        self.assertTrue(r2.overlaps(r1))  # Should be symmetric

    def test_overlaps_touching_at_boundary(self):
        """Test ranges that touch at a boundary (inclusive)."""
        r1 = Range(1, 17)
        r2 = Range(17, 29)
        # Since ranges are inclusive, 17 is in both ranges
        self.assertTrue(r1.overlaps(r2))
        self.assertTrue(r2.overlaps(r1))

    def test_overlaps_adjacent_no_overlap(self):
        """Test adjacent ranges that don't overlap."""
        r1 = Range(1, 17)
        r2 = Range(18, 29)
        self.assertFalse(r1.overlaps(r2))
        self.assertFalse(r2.overlaps(r1))

    def test_overlaps_completely_separate(self):
        """Test completely separate ranges."""
        r1 = Range(1, 10)
        r2 = Range(20, 30)
        self.assertFalse(r1.overlaps(r2))
        self.assertFalse(r2.overlaps(r1))

    def test_overlaps_one_contains_other(self):
        """Test when one range completely contains another."""
        r1 = Range(1, 30)
        r2 = Range(10, 20)
        self.assertTrue(r1.overlaps(r2))
        self.assertTrue(r2.overlaps(r1))

    def test_overlaps_identical_ranges(self):
        """Test identical ranges."""
        r1 = Range(5, 15)
        r2 = Range(5, 15)
        self.assertTrue(r1.overlaps(r2))

    def test_overlaps_single_point(self):
        """Test ranges with single-point overlap."""
        r1 = Range(1, 10)
        r2 = Range(10, 20)
        self.assertTrue(r1.overlaps(r2))

    def test_overlaps_single_value_ranges(self):
        """Test single-value ranges."""
        r1 = Range(5, 5)
        r2 = Range(5, 5)
        r3 = Range(6, 6)
        self.assertTrue(r1.overlaps(r2))
        self.assertFalse(r1.overlaps(r3))


class TestRangeMerge(unittest.TestCase):
    """Test cases for Range.merge method."""

    def test_merge_standard_overlap(self):
        """Test merging standard overlapping ranges."""
        r1 = Range(1, 17)
        r2 = Range(13, 29)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(1, 29))
        # Verify symmetry
        merged2 = r2.merge(r1)
        self.assertEqual(merged2, Range(1, 29))

    def test_merge_touching_at_boundary(self):
        """Test merging ranges that touch at boundary."""
        r1 = Range(1, 17)
        r2 = Range(17, 29)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(1, 29))

    def test_merge_one_contains_other(self):
        """Test merging when one range contains another."""
        r1 = Range(1, 30)
        r2 = Range(10, 20)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(1, 30))
        # Test reverse
        merged2 = r2.merge(r1)
        self.assertEqual(merged2, Range(1, 30))

    def test_merge_identical_ranges(self):
        """Test merging identical ranges."""
        r1 = Range(5, 15)
        r2 = Range(5, 15)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(5, 15))

    def test_merge_partial_overlap(self):
        """Test merging ranges with partial overlap."""
        r1 = Range(5, 15)
        r2 = Range(10, 20)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(5, 20))

    def test_merge_single_point_overlap(self):
        """Test merging ranges with single point overlap."""
        r1 = Range(1, 10)
        r2 = Range(10, 20)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(1, 20))

    def test_merge_non_overlapping_raises_error(self):
        """Test that merging non-overlapping ranges raises ValueError."""
        r1 = Range(1, 10)
        r2 = Range(15, 20)
        with self.assertRaises(ValueError):
            r1.merge(r2)

    def test_merge_adjacent_non_overlapping_raises_error(self):
        """Test that merging adjacent but non-overlapping ranges raises ValueError."""
        r1 = Range(1, 17)
        r2 = Range(18, 29)
        with self.assertRaises(ValueError):
            r1.merge(r2)

    def test_merge_single_value_ranges(self):
        """Test merging single-value ranges."""
        r1 = Range(5, 5)
        r2 = Range(5, 5)
        merged = r1.merge(r2)
        self.assertEqual(merged, Range(5, 5))


class TestContainedInRanges(unittest.TestCase):
    """Test cases for the contained_in_ranges function."""

    def setUp(self):
        """Set up test ranges from the problem example."""
        # Example ranges: 3-5, 10-14, 16-20, 12-18
        self.ranges = [
            Range(3, 5),
            Range(10, 14),
            Range(16, 20),
            Range(12, 18)
        ]

    def test_value_in_single_range(self):
        """Test value contained in exactly one range."""
        self.assertTrue(contained_in_ranges(5, self.ranges))  # In 3-5
        self.assertTrue(contained_in_ranges(11, self.ranges))  # In 10-14

    def test_value_in_overlapping_ranges(self):
        """Test value contained in multiple overlapping ranges."""
        # 17 is in both 16-20 and 12-18
        self.assertTrue(contained_in_ranges(17, self.ranges))
        # 13 is in both 10-14 and 12-18
        self.assertTrue(contained_in_ranges(13, self.ranges))

    def test_value_not_in_any_range(self):
        """Test value not contained in any range."""
        self.assertFalse(contained_in_ranges(1, self.ranges))
        self.assertFalse(contained_in_ranges(8, self.ranges))
        self.assertFalse(contained_in_ranges(32, self.ranges))

    def test_empty_ranges_list(self):
        """Test with empty ranges list."""
        self.assertFalse(contained_in_ranges(5, []))

    def test_example_from_problem(self):
        """Test all values from the problem example."""
        # From problem: "3 of the available ingredient IDs are fresh"
        values_and_expected = [
            (1, False),   # spoiled
            (5, True),    # fresh (3-5)
            (8, False),   # spoiled
            (11, True),   # fresh (10-14)
            (17, True),   # fresh (16-20 and 12-18)
            (32, False),  # spoiled
        ]

        for value, expected_fresh in values_and_expected:
            with self.subTest(value=value):
                self.assertEqual(
                    contained_in_ranges(value, self.ranges),
                    expected_fresh,
                    f"Ingredient ID {value} should be {'fresh' if expected_fresh else 'spoiled'}"
                )


class TestGetInputs(unittest.TestCase):
    """Test cases for the get_inputs function."""

    def test_example_input(self):
        """Test parsing the example from the problem."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        # Check ranges
        self.assertEqual(len(ranges), 4)
        self.assertEqual(ranges[0].start, 3)
        self.assertEqual(ranges[0].end, 5)
        self.assertEqual(ranges[1].start, 10)
        self.assertEqual(ranges[1].end, 14)
        self.assertEqual(ranges[2].start, 16)
        self.assertEqual(ranges[2].end, 20)
        self.assertEqual(ranges[3].start, 12)
        self.assertEqual(ranges[3].end, 18)

        # Check values
        self.assertEqual(values, [1, 5, 8, 11, 17, 32])

    def test_empty_input(self):
        """Test parsing empty input."""
        fileobj = io.StringIO("")
        ranges, values = get_inputs(fileobj)

        self.assertEqual(len(ranges), 0)
        self.assertEqual(len(values), 0)

    def test_only_ranges(self):
        """Test input with only ranges, no values."""
        input_text = """1-5
10-15
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        self.assertEqual(len(ranges), 2)
        self.assertEqual(len(values), 0)

    def test_only_values(self):
        """Test input with only values, no ranges."""
        input_text = """5
10
15
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        self.assertEqual(len(ranges), 0)
        self.assertEqual(values, [5, 10, 15])

    def test_blank_lines_ignored(self):
        """Test that blank lines are properly ignored."""
        input_text = """1-5

10
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        self.assertEqual(len(ranges), 1)
        self.assertEqual(len(values), 1)

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        input_text = """  3-5
  10
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        self.assertEqual(len(ranges), 1)
        self.assertEqual(ranges[0].start, 3)
        self.assertEqual(ranges[0].end, 5)
        self.assertEqual(values, [10])


class TestMergeRanges(unittest.TestCase):
    """Test cases for the merge_ranges function."""

    def test_merge_empty_list(self):
        """Test merging an empty list."""
        result = merge_ranges([])
        self.assertEqual(result, [])

    def test_merge_single_range(self):
        """Test merging a list with a single range."""
        result = merge_ranges([Range(1, 10)])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Range(1, 10))

    def test_merge_non_overlapping_ranges(self):
        """Test merging non-overlapping ranges."""
        ranges = [Range(1, 5), Range(10, 15), Range(20, 25)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], Range(1, 5))
        self.assertEqual(result[1], Range(10, 15))
        self.assertEqual(result[2], Range(20, 25))

    def test_merge_overlapping_ranges(self):
        """Test merging overlapping ranges."""
        ranges = [Range(1, 10), Range(5, 15)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Range(1, 15))

    def test_merge_touching_ranges(self):
        """Test merging ranges that touch at boundary."""
        ranges = [Range(1, 10), Range(10, 20)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Range(1, 20))

    def test_merge_multiple_overlapping(self):
        """Test merging multiple overlapping ranges from the example."""
        ranges = [Range(3, 5), Range(10, 14), Range(16, 20), Range(12, 18)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], Range(3, 5))
        self.assertEqual(result[1], Range(10, 20))

    def test_merge_unsorted_ranges(self):
        """Test that merge_ranges works with unsorted input."""
        ranges = [Range(20, 25), Range(1, 5), Range(10, 15)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], Range(1, 5))
        self.assertEqual(result[1], Range(10, 15))
        self.assertEqual(result[2], Range(20, 25))

    def test_merge_all_into_one(self):
        """Test merging ranges that all overlap into one."""
        ranges = [Range(1, 10), Range(5, 15), Range(12, 20), Range(18, 25)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Range(1, 25))

    def test_merge_duplicate_ranges(self):
        """Test merging duplicate ranges."""
        ranges = [Range(1, 10), Range(1, 10), Range(20, 30)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], Range(1, 10))
        self.assertEqual(result[1], Range(20, 30))

    def test_merge_one_contains_others(self):
        """Test merging when one range contains all others."""
        ranges = [Range(1, 100), Range(10, 20), Range(30, 40), Range(50, 60)]
        result = merge_ranges(ranges)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Range(1, 100))


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components."""

    def test_full_example_part1(self):
        """Test the complete example from the problem - Part 1."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        # Count fresh ingredients
        fresh_count = sum(1 for v in values if contained_in_ranges(v, ranges))

        # Should be 3 fresh ingredients (5, 11, 17)
        self.assertEqual(fresh_count, 3)

    def test_full_example_part2(self):
        """Test the complete example from the problem - Part 2."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
        fileobj = io.StringIO(input_text)
        ranges, values = get_inputs(fileobj)

        # Merge ranges
        merged = merge_ranges(ranges)

        # Should have 2 merged ranges: 3-5 and 10-20
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0], Range(3, 5))
        self.assertEqual(merged[1], Range(10, 20))

        # Calculate total length
        total_length = sum(r.length() for r in merged)
        # 3-5 has length 3, 10-20 has length 11, total = 14
        self.assertEqual(total_length, 14)


if __name__ == '__main__':
    unittest.main()
